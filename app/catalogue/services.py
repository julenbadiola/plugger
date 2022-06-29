
import os
from pathlib import Path
import json
import yaml
from .schema import ServiceModel

PROTOCOL = "http://"
DOMAIN = "localhost"
OUTPUTS = {
    "DOMAIN": DOMAIN,
    "PROTOCOL": PROTOCOL,
    "COMPLETE_PATH": PROTOCOL + DOMAIN,
    "PUBLIC_NETWORK": os.getenv("NETWORK_NAME")
}
ALL = {}

def parse_and_add_data(data: dict):
    try:
        ServiceModel(**data)
        ALL[data["key"]] = data
    except Exception as e:
        key = data.get("key", "unknown")
        print(f"An error happened when trying to parse {key}")
        print(str(e))

# Iterates among json and yaml files in /services folder
for path in Path("/app/services").glob('**/*.json'):
    f = open(str(path))
    data = json.load(f)
    parse_and_add_data(data)
    f.close()

for path in Path("/app/services").glob('**/*.yaml'):
    f = open(str(path))
    data = yaml.safe_load(f)
    parse_and_add_data(data)
    f.close()

# Get outputs of all services
for k, v in ALL.items():
    for var in v.get("variables", []):
        OUTPUTS[var["key"]] = var["value"]

# Substitute the outputs keys with the outputs values
def substitute(obj):
    obj_type = type(obj)
    if obj_type == str:
        # Check if there is a reference to an output and replace it with its value
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
