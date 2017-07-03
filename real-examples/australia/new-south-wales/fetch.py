import json
import optparse
from pprint import pprint

from pyquery import PyQuery as pq
import requests


def writeFile(fname, data, url):
    try:
        with open(fname, 'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        with open("errors.txt", 'a') as err:
            print("Failed to write %s, %s" % (fname, e))
            err.write(
                "Failed to write %s, %s, %s\n" % (fname, e, url))


def writeReleases(releases, folder, data, url):
    for i, r in enumerate(releases):
        r['packageInfo'] = {
            'uri': None,  # This publisher does not supply a URI.
            'publishedDate': data['publishedDate'],
            'publisher': data['publisher']
        }
        fname = '%s/releases/%s-%s.json' % (folder, r['ocid'], r['id'])
        writeFile(fname, r, url)
        if folder == 'sample' and i >= 10:
            break


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'https://tenders.nsw.gov.au'
    url += '/?event=public.api.%s.search&ResultsPerPage=1000'
    # planning, tender, contract
    if options.all:
        release_types = ['planning', 'tender', 'contract']
        for r in release_types:
            next_url = url % r
            while next_url:
                print('fetching', next_url)
                r = requests.get(next_url)
                data = r.json()
                writeReleases(data['releases'], 'all', data, next_url)
                if 'next' in data['links']:
                    next_url = data['links']['next']
                else:
                    next_url = None
    else:
        next_url = url % 'planning'
        r = requests.get(next_url)
        data = r.json()
        writeReleases(data['releases'], 'sample', data, next_url)

if __name__ == '__main__':
    main()
