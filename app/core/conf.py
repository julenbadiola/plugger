import os

COMPOSE = os.getenv('MODE', "compose") == "compose"
NETWORK_NAME = os.getenv('NETWORK_NAME', "public-net")
DOMAIN = os.getenv('DOMAIN', "localhost")

PROTOCOL = "http://"
DOMAIN = os.getenv('DOMAIN', "localhost")
FULL_PATH = PROTOCOL + DOMAIN