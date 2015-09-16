import os
import jsonmerge
import json

with open('../../standard/standard/schema/release-schema.json', 'r') as f:
    release_schema = json.load(f)

compiled_release = {}
versioned_release = {}
releases = []
package = None

# Get all the JSON files in this directory
for fname in sorted(os.listdir(".")):
    if fname.endswith('json'):
        with open(fname, 'r') as jsonfile:
            package = json.load(jsonfile)
            for release in package['releases']:
                releases.append({
                    'url': package['uri'] + '#' + release['id'],
                    'date': release['date'],
                    'tag': release['tag']
                })
                versioned_release = jsonmerge.merge(versioned_release, release, release_schema)
                compiled_release = jsonmerge.merge(compiled_release, release)

with open("record/ocds-213czf-000-00001.json", 'w') as f:
    json.dump({
        'uri': 'http://standard.open-contracting.org/examples/records/ocds-213czf-000-00001.json',
        'packages': [package['uri']],
        'publisher': package['publisher'],
        'publishedDate': '2009-03-15',
        'records': [{
            'ocid': 'ocds-213czf-000-00001',
            'releases': releases,
            'compiledRelease': compiled_release,
            'versionedRelease': versioned_release,
        }]
    }, f, indent=3, sort_keys=True)
