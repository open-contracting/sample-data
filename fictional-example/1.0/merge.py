import os
import json
import ocdsmerge

releases = []
release_list = []
packages = []
package = None

# Get all the JSON files in this directory
for fname in sorted(os.listdir(".")):
    if fname.endswith('json'):
        with open(fname, 'r') as jsonfile:
            package = json.load(jsonfile)
            for release in package['releases']:
                packages.append(package['uri'] + '#' + release['id'])
                releases.append({
                    'url': package['uri'] + '#' + release['id'],
                    'date': release['date'],
                    'tag': release['tag']
                })
                release_list.append(release)

compiled_release = ocdsmerge.merge(release_list)

versioned_release = ocdsmerge.merge_versioned(release_list)

with open("record/ocds-213czf-000-00001.json", 'w') as f:
    json.dump({
        'uri': 'http://standard.open-contracting.org/examples/records/ocds-213czf-000-00001.json',
        'packages': packages,
        'publisher': package['publisher'],
        'publishedDate': '2014-02-02T13:02:00Z',
        'records': [{
            'ocid': 'ocds-213czf-000-00001',
            'releases': releases,
            'compiledRelease': compiled_release,
        }]
    }, f, indent=2, sort_keys=True)
    f.write('\n')

with open("record/ocds-213czf-000-00001-withversions.json", 'w') as f:
    json.dump({
        'uri': 'http://standard.open-contracting.org/examples/records/ocds-213czf-000-00001.json',
        'packages': packages,
        'publisher': package['publisher'],
        'publishedDate': '2014-02-02T13:02:00Z',
        'records': [{
            'ocid': 'ocds-213czf-000-00001',
            'releases': releases,
            'compiledRelease': compiled_release,
            'versionedRelease': versioned_release,
        }]
    }, f, indent=2, sort_keys=True)
    f.write('\n')
