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
    releases = data['releases']
    for i, r in enumerate(releases):
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
    return releases


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'https://ville.montreal.qc.ca/vuesurlescontrats/api/releases.json'
    more_releases = True
    offset = 0
    if options.all:
        while more_releases:
            next_url = url + '?limit=10000&offset=%s' % offset
            more_releases = len(fetchReleases(next_url, 'all'))
            offset += 10000
    else:
        url += '?limit=10'
        fetchReleases(url, 'sample')

if __name__ == '__main__':
    main()
