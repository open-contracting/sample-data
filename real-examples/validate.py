import glob
import json
import optparse

import requests
from jsonschema import validate

'''
Validate a set of JSON files against a given OCDS schema.
'''


def get_schema(name, version):
    version = '__'.join(version.split('.'))
    url = 'http://standard.open-contracting.org/schema/'
    url += '%s/%s' % (version, name)
    r = requests.get(url)
    print(url)
    return r.json()


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-f', '--filepath', action='store', default=None,
                      help='Path to files, e.g. paraguay/sample')
    parser.add_option('-v', '--version', action='store', default='1.1.0',
                      help='Version, e.g. 1.1.0')
    parser.add_option(
        '-t', '--type', action='store', default='release',
        help='File type: release-package, record-package or release')
    (options, args) = parser.parse_args()
    if not options.filepath:
        parser.error('You must supply a filepath, using the -f argument')
    schema = get_schema('%s-schema.json' % options.type, options.version)
    if options.type == 'record-package' and options.version == '1.1.0':
        # Fix v1.1 schema error - wrong item is required.
        schema['required'].remove('releases')
        schema['required'].append('records')
    for filename in glob.glob('%s/*.json' % options.filepath):
        if not filename.endswith('.json'):
            print('Skipping non-JSON file %s' % filename)
            continue
        with open(filename, 'r') as file:
            # print('\n%s' % filename)
            try:
                data = json.load(file)
            except Exception as e:
                print('Problem loading', filename)
                print(e)
                continue
            try:
                validate(data, schema)
            except Exception as e:
                print('\nProblem validating', filename)
                location = '/'.join(e.absolute_schema_path)
                message = e.message
                print("%s: %s" % (location, message))
                data['validationErrors'] = str("%s: %s" % (location, message))
            with open(filename, 'w') as writefile:
                writefile.write(json.dumps(data, indent=2))

if __name__ == '__main__':
    main()
