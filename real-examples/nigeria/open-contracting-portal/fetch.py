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


def writeReleases(releases, folder, data, url):
    for i, r in enumerate(releases):
        r['packageInfo'] = {
            'uri': data['uri'],
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
    url = 'http://35.160.38.216/downloadSelected'
    r = requests.get(url)
    data = r.json()
    if options.all:
        folder = 'all'
    else:
        folder = 'sample'
    writeReleases(data['releases'], folder, data, url)


if __name__ == '__main__':
    main()
