import os
import jsonmerge
import json

with open('../../standard/standard/schema/release-schema.json', 'r') as f:
    release_schema = json.load(f)

base = {}

# Get all the JSON files in this directory
for fname in sorted(os.listdir(".")):
    if fname.endswith('json'):
        print(fname)
        with open(fname, 'r') as jsonfile:
            package = json.load(jsonfile)
            for release in package['releases']:
                base = jsonmerge.merge(base, release, release_schema)

with open("record/record.json", 'w') as f:
    json.dump(base, f, indent=3, sort_keys=True)
