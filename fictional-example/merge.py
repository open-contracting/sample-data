import os
import jsonmerge
import json
from jsonschema import validate
from collections import defaultdict
from operator import itemgetter
from copy import deepcopy

with open('../../standard/standard/schema/release-schema.json', 'r') as f:
    release_schema = json.loads(f.read())

contacting_processes = {}

# Get all the JSON files in this directory
for f in os.listdir("."):
    if f.endswith('json'):
        with open(f,'r') as jsonfile:
            package = json.loads(jsonfile.read())
            for release in package['releases']:
                try:
                    base
                except:
                    base = release
                    
                base = jsonmerge.merge(base, release, release_schema)


with open("record/record.json", 'w') as f:
    f.write(json.dumps(base,indent=3))