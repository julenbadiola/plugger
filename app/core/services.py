
import os
from pathlib import Path
import json
import yaml
from .service import ServiceModel

PROTOCOL = "http://"
DOMAIN = "localhost"
OUTPUTS = {
    "DOMAIN": DOMAIN,
    "PROTOCOL": PROTOCOL,
    "COMPLETE_PATH": PROTOCOL + DOMAIN,
    "PUBLIC_NETWORK": os.getenv("NETWORK_NAME")
}
ALL = {}

# Iterates among json and yaml files in /services folder
for path in Path("/app/services").glob('**/*.json'):
    f = open(str(path))
    data = json.load(f)
    
    ServiceModel(**data)

    ALL[data["key"]] = data
    f.close()
for path in Path("/app/services").glob('**/*.yaml'):
    f = open(str(path))
    data = yaml.safe_load(f)
    
    ServiceModel(**data)

    ALL[data["key"]] = data
    f.close()

# Get outputs of all services
for k, v in ALL.items():
    for var in v.get("variables", []):
        OUTPUTS[var["key"]] = var["value"]

def substitute(obj):
    obj_type = type(obj)
    if obj_type == str:
        new_str = obj
        for varkey, varvalue in OUTPUTS.items():
            new_str = new_str.replace(f"##{varkey}##", varvalue)
        return new_str
    elif obj_type == dict:
        new_obj = {}
        for key, value in obj.items():
            new_obj[key] = substitute(value)
        return new_obj
    elif obj_type == list:
        new_list = []
        for value in obj:
            new_list.append(substitute(value))
        return new_list
    else:
        return obj


# Substitutes the references to outputs
SERVICES_LIST = substitute(ALL)
