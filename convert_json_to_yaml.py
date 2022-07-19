import yaml
import json
from pathlib import Path

# Iterates among json files in /services folder and converts them to yaml
for path in Path(".").glob('**/*.json'):
    f = open( str(path))
    data = json.load(f)
    print(path)
    ff = open(str(path).replace(".json", ".yaml"), 'w+')
    yaml.dump(data, ff, allow_unicode=True)
    f.close()
    ff.close()

# for path in Path(".").glob('**/*.yaml'):
#     f = open( str(path))
#     data = yaml.safe_load(f)