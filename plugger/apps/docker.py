import docker
from docker.models.containers import Container
from docker.errors import NotFound
import os
from core.catalogue import PLUGINS_LIST, DOMAIN, PROTOCOL

COMPOSE = os.getenv('MODE', "compose") == "compose"
# "compose" or "swarm"

docker_client = docker.from_env()

class NetworkManager:
    resume = {}

    def __init__(self) -> None:
        for network in self.list():
            self.resume[network.name] = network.id
        print(self.resume)

    def list(self):
        return docker_client.networks.list()

    def get(self, id):
        return docker_client.networks.get(id)

    def create(self, name):
        print("Creating network", name)
        obj = docker_client.networks.create(name=name, scope="global" if COMPOSE else "swarm")
        self.resume[name] = obj.id

    def remove(self, name):
        print("Removing network", name)
        obj = self.get(self.resume[name])
        if obj:
            obj.remove()
        del self.resume[name]

network_manager = NetworkManager()

class ServiceManager:
    resume = {}

    def __init__(self) -> None:
        for service in self.list():
            self.resume[service.name] = service.id
            if COMPOSE and service.name == "plugger":
                self.compose_project = service.labels.get("com.docker.compose.project")
        print(self.resume)

    def list(self):
        if COMPOSE:
            return docker_client.containers.list()
        return docker_client.services.list()

    def get(self, id):
        if COMPOSE:
            return docker_client.containers.get(id)
        return docker_client.services.get(id)

    def start(self, name, plugin: dict, env: list):
        try:
            existent = self.get(name)
            self.remove(existent)
        except NotFound:
            pass

        if plugin.get("pull", True):
            docker_client.images.pull(plugin.get("image"))

        for dependency_name in plugin.get("dependencies", []):
            dependency = PLUGINS_LIST[dependency_name]

            try:
                self.get(dependency_name)
                print(f"Dependency {dependency_name} already started")
            except NotFound:
                depenv = [i["key"] + "=" + i["value"] for i in dependency.get("configuration", {}).get("system", [])]
                self.start(name=dependency_name, plugin=dependency, env=depenv)              

        print("Starting service", name)
        net_name = plugin.get("network")
        if not network_manager.get(net_name):
            network_manager.create(name=net_name)

        # If in compose
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

        if COMPOSE:
            labels["com.docker.compose.project"] = self.compose_project
            return docker_client.containers.run(
                image=plugin.get("image"),
                detach=True,
                name=name,
                labels=labels,
                environment=env,
                network=net_name
            )
        # If in swarm
        return docker_client.services.create(
            image=plugin.get("image"),
            name=name,
            labels=plugin.get("labels"),
            environment=env,
            networks=[net_name]
        )

    def remove(self, id):
        try:
            obj = self.get(id)
            print("Removing service", obj.name)
            obj.stop()
            obj.remove()
        except NotFound:
            pass

    # @lru_cache() ttl_hash=5
    def status(self):
        started = []
        notstarted = []
        
        for name, plugin in PLUGINS_LIST.items():
            plugin["name"] = name
            if plugin.get("show", True):
                for container in self.list():
                    if plugin.get("image") in container.image.attrs.get("RepoTags"):
                        if traefik_conf := plugin.get("configuration", {}).get("routing", {}).get("traefik", {}):
                            plugin["route"] = PROTOCOL + DOMAIN + traefik_conf.get("prefix")
                        started.append(plugin)
                        break
                else:
                    notstarted.append(plugin)
            
        return started, notstarted

manager = ServiceManager()
