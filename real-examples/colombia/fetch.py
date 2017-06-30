import json
import optparse

import requests
from pprint import pprint


def writeFile(fname, data, url):
    try:
        with open(fname, 'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        with open("errors.txt", 'a') as err:
            print("Failed to write %s, %s" % (fname, e))
            err.write(
                "Failed to write %s, %s, %s\n" % (fname, e, url))


def fetchReleases(data, folder, url):
    print('Fetching %s' % url)
    for i, r in enumerate(data['releases']):
        # These release packages lack URIs and dates.
        r['packageInfo'] = {
            'uri': None,
            'publishedDate': None,
            'publisher': data['publisher']
        }
        fname = '%s/releases/%s-%s.json' % \
            (folder, r['ocid'].replace('/', '_'), r['id'].replace('/', '_'))
        print(fname)
        writeFile(fname, r, url)


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'https://api.colombiacompra.gov.co/releases/'
    if options.all:
        next_url = url
        while next_url:
            # TODO: Add error handling, there are 400k pages to download.
            r = requests.get(next_url)
            data = r.json()
            fetchReleases(data, 'all', next_url)
            next_url = data['links']['next']
    else:
        r = requests.get(url)
        data = r.json()
        fetchReleases(data, 'sample', url)

if __name__ == '__main__':
    main()
