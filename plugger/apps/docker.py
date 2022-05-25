import docker
from docker.models.containers import Container
from docker.errors import NotFound
import os

COMPOSE = os.getenv('MODE', "compose") == "compose"
# "compose" or "swarm"

class ServiceManager:
    def __init__(self) -> None:
        self.client = docker.from_env()
        
    def list(self):
        if COMPOSE:
            return self.client.containers.list()
        return self.client.services.list()

    def get(self, id):
        if COMPOSE:
            return self.client.containers.get(id)
        return self.client.services.get(id)

    def start(self, plugin, env):
        try:
            existent = self.get(plugin.get("name"))
            self.remove(existent)
        except NotFound:
            pass
        self.client.images.pull(plugin.get("image"))

        # If in compose
        if COMPOSE:
            return self.client.containers.run(
                image=plugin.get("image"),
                detach=True,
                name=plugin.get("name"),
                labels=plugin.get("labels"),
                environment=plugin.get("env") + env,
                network="tfm_web_network"
            )
        # If in swarm
        return self.client.services.create(
            image=plugin.get("image"),
            name=plugin.get("name"),
            labels=plugin.get("labels"),
            environment=plugin.get("env") + env,
            networks=["tfm_web_network"]
        )

    def remove(self, object):
        return object.remove()

manager = ServiceManager()