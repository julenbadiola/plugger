from ctypes import Union
import docker
from docker.models.containers import Container
from docker.models.networks import Network
from docker.errors import NotFound
import os
from core.services import SERVICES_LIST, DOMAIN, PROTOCOL

COMPOSE = os.getenv('MODE', "compose") == "compose"
# "compose" or "swarm"

docker_client = docker.from_env()

class NetworkManager:
    resume = {}

    def __init__(self) -> None:
        for network in self.list():
            self.resume[network.name] = network.id
        # print(self.resume)

    def list(self):
        return docker_client.networks.list()

    def get(self, id: str):
        return docker_client.networks.get(id)

    def connect(self, network, container):
        if type(network) != Network:
            network = self.get(id=network)
        return network.connect(container)

    def create(self, name: str):
        print("Creating network", name)
        return docker_client.networks.create(name=name, scope="global" if COMPOSE else "swarm")

    def remove(self, network):
        if type(network) != Network:
            network = self.get(network)
        
        print("Removing network", network.name)
        if network:
            return network.remove()

network_manager = NetworkManager()

def get_environment(plugin, additional_environment_variables):
    # Get environment variables of the plugin
    env_list = plugin.get("configuration", {}).get("environment", [])
    # Create a env list for all the environment variables
    env = []
    for environment_variable in env_list:
        key = environment_variable["key"]
        value = ""
        # first check if in POST data if the variable is editable
        if environment_variable.get("editable", False):
            if form_value := additional_environment_variables.get(key, None):
                value = form_value
                
        # If not value, get the value by default
        if not value:
            value = environment_variable.get("value", None)
        
        # If there is no value yet and the variable is not optional, raise Exception
        if not value and not environment_variable.get("optional", False):
            raise Exception(f"Value for {key} not present")
        env.append(key + "=" + value)
    return env

class ServiceManager:
    resume = {}

    def __init__(self) -> None:
        for service in self.list():
            self.resume[service.name] = service.id
            if COMPOSE and service.name == "plugger":
                self.compose_project = service.labels.get("com.docker.compose.project")
        # print(self.resume)

    def list(self):
        if COMPOSE:
            return docker_client.containers.list()
        return docker_client.services.list()

    def get(self, id: str):
        if COMPOSE:
            return docker_client.containers.get(id)
        return docker_client.services.get(id)

    def start(self, name, plugin: dict, additional_environment_variables: dict):
        # Check if already exists a container with the name in parameters and remove it
        try:
            existent = self.get(name)
            self.remove(container=existent)
        except NotFound:
            pass
        
        # Pull docker image (can be false to use local images)
        if plugin.get("pull", True):
            docker_client.images.pull(plugin.get("image"))

        # Check the dependencies of the container and start them
        for dependency_name in plugin.get("dependencies", []):
            dependency = SERVICES_LIST[dependency_name]

            try:
                self.get(dependency_name)
                print(f"Dependency {dependency_name} already started")
            except NotFound:
                self.start(name=dependency_name, plugin=dependency, additional_environment_variables={})              

        # Start
        print("Starting service", name)

        # Create the network if it does not exist
        net_name = plugin.get("network")
        try:
            net = network_manager.get(net_name)
        except NotFound:
            net = network_manager.create(name=net_name)

        # Add the labels for the traefik routing if needed
        labels = plugin.get("labels", {})
        
        if traefik_conf := plugin.get("configuration", {}).get("routing", {}).get("traefik", {}):
            labels["traefik.enable"] = "true"
            prefix = traefik_conf.get("prefix")
            inner_port = traefik_conf.get("prefix")
            labels[f"traefik.http.routers.tfm-{name}.rule"] = f"Host(`{DOMAIN}`) && PathPrefix(`{prefix}`)"
            labels[f"traefik.http.services.tfm-{name}.loadbalancer.server.port"] = str(inner_port)
            strip = traefik_conf.get("strip", False)
            if strip:
                labels[f"traefik.http.middlewares.{name}-stripprefix.stripprefix.prefixes"] = prefix
                labels[f"traefik.http.routers.tfm-{name}.middlewares"] = f"{name}-stripprefix"
        
        # Map the ports structure
        ports = {mapping["from"]:mapping["to"] for mapping in plugin.get("configuration", {}).get("routing", {}).get("ports", [])}

        # If in compose, create a container
        if COMPOSE:
            labels["com.docker.compose.project"] = self.compose_project
            return docker_client.containers.run(
                image=plugin.get("image"),
                detach=True,
                name=name,
                labels=labels,
                environment=get_environment(plugin, additional_environment_variables),
                ports=ports,
                network=net_name
            )
        # If in swarm, create a service
        return docker_client.services.create(
            image=plugin.get("image"),
            name=name,
            labels=plugin.get("labels", None),
            ports=ports,
            environment=get_environment(plugin, additional_environment_variables),
            networks=[net_name]
        )

    def remove(self, container):
        try:
            # try to get container object if the parameter is not of container type
            if type(container) != Container:
                container = self.get(container)

            print("Removing service", container.name)

            # dependencies of the container to be removed
            dependencies = SERVICES_LIST[container.name].get("dependencies", [])
            
            container.stop()
            container.remove()
            
            # remove unused dependencies
            for dependency in dependencies:
                self.remove(dependency)
        except NotFound:
            pass

    # @lru_cache() ttl_hash=5
    def status(self):
        started = []
        notstarted = []
        
        containers = self.list()

        for name, plugin in SERVICES_LIST.items():
            plugin["name"] = name
            if plugin.get("hide", False):
                continue

            for container in containers:
                if plugin.get("image") in container.image.attrs.get("RepoTags"):
                    
                    if traefik_conf := plugin.get("configuration", {}).get("routing", {}).get("traefik", {}):
                        plugin["route"] = PROTOCOL + DOMAIN + traefik_conf.get("prefix")
                    
                    elif ports_conf := plugin.get("configuration", {}).get("routing", {}).get("ports", {}):
                        plugin["route"] = PROTOCOL + DOMAIN + ":" + ports_conf[0].get("to")
                    
                    started.append(plugin)
                    break
            else:
                notstarted.append(plugin)
            
        return started, notstarted

manager = ServiceManager()
