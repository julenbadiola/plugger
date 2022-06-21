from pydantic import BaseModel, Extra, root_validator, validator
from typing import List, Dict, Optional

class TraefikConfig(BaseModel):
    inner_port: int
    prefix: str
    strip: Optional[bool]

class RoutingConfigurationSection(BaseModel):
    traefik: Optional[TraefikConfig]
    ports: Optional[Dict[str, str]]

class ConfigurationSection(BaseModel):
    environment: Optional[List[Dict[str, str]]]
    routing: Optional[RoutingConfigurationSection]

class InfoSection(BaseModel, extra=Extra.allow):
    icon: str
    name: str
    description: str
    snapshots: List[str]

class Variable(BaseModel, extra=Extra.forbid):
    key: str
    value: str
    output: Optional[bool]

class ServiceModel(BaseModel, extra=Extra.forbid):
    configuration: ConfigurationSection
    dependencies: List[str]
    image: str
    info: Optional[InfoSection]
    key: str
    network: str

    # Variables
    variables: List[Dict[str, str]]
    
    # Pull image from registry or use local
    pull: Optional[bool]

    # Hide the service in the catalogue
    hide: Optional[bool]

    # Additional labels for the container
    labels: Optional[dict]

    @root_validator(pre=True)
    def check_card_number_omitted(cls, values):
        if not values.get("hide", False) and not values.get("info"):
            raise ValueError("Info mandatory when hide is true", values)
        return values