import glob
import json
import optparse

import requests
from jsonschema import validate

'''
Validate a set of JSON files against a given OCDS schema.
'''


def get_schema(name):
    url = 'http://standard.open-contracting.org/schema/'
    url += '1__1__0/%s' % name
    r = requests.get(url)
    return r.json()


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-f', '--filepath', action='store', default=None,
                      help='Path to files, e.g. paraguay/sample')
    parser.add_option(
        '-t', '--type', action='store', default='release-package',
        help='File type: release-package, record-package or release')
    (options, args) = parser.parse_args()
    if not options.filepath:
        parser.error('You must supply a filepath, using the -f argument')
    schema = get_schema('%s-schema.json' % options.type)
    for filename in glob.glob('%s/*.json' % options.filepath):
        if not filename.endswith('.json'):
            print('Skipping non-JSON file %s' % filename)
            continue
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
            except Exception as e:
                print('Problem loading', filename)
                print(e)
                continue
            try:
                validate(data, schema)
            except Exception as e:
                print('Problem validating', filename)
                data['validationErrors'] = str(e)
            with open(filename, 'w') as writefile:
                writefile.write(json.dumps(data, indent=2))

if __name__ == '__main__':
    main()
