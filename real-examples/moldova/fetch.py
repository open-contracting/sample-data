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
        fname = '%s/releases/%s-%s.json' % (folder, r['ocid'], r['id'])
        writeFile(fname, r, url)
        if folder == 'sample' and i >= 50:
            break


def fetchYears(url):
    r = requests.get(url)
    # Hack to fix invalid JSON.
    content = str(r.content.decode('utf8')).replace(
        '/year/2012",', '/year/2012"')
    data = json.loads(content)
    return data['links']['all']


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    BASE = 'http://moldova-ocds.yipl.com.np'
    if options.all:
        url = '%s/multiple-file-api/releases.json' % BASE
        years = fetchYears(url)
        for year in years:
            fetchReleases(year, 'all')
    else:
        url = '%s/ocds-api/year/2017' % BASE
        fetchReleases(url, 'sample')

if __name__ == '__main__':
    main()
