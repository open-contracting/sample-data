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


def fetchReleases(url, folder):
    print("Fetching releases for %s" % url)
    r = requests.get(url)
    data = r.json()
    for i, r in enumerate(data['releases']):
        r['packageInfo'] = {
            'uri': data['uri'],
            'publishedDate': data['publishedDate'],
            'publisher': data['publisher']
        }
        fname = '%s/releases/%s-%s.json' % \
            (folder, r['ocid'].replace('/', '_'), r['id'].replace('/', '_'))
        writeFile(fname, r, url)
        if folder == 'sample' and i >= 10:
            break


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    BASE = 'https://buyandsell.gc.ca'
    if options.all:
        # No new data is being published, so just get the four
        # years that exist.
        urls = []
        for i in range(13, 17):
            url = '%s/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-%s-%s.json' \
                % (BASE, i, i+1)
            urls.append(url)
        for url in urls:
            fetchReleases(url, 'all')
    else:
        url = '%s/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-15-16.json' % BASE
        fetchReleases(url, 'sample')

if __name__ == '__main__':
    main()
