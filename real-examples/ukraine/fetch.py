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
    BASE = 'http://ocds.prozorro.openprocurement.io'
    if options.all:
        r = requests.get(BASE)
        d = pq(r.content)
        links = d('.container ol li a')
        latest_url = "%s/%s" % (BASE, links[-2].attrib['href'])
        if 'with_extensions' in latest_url:
            r = requests.get(latest_url)
            d = pq(r.content)
            links = d('.container ol li a')
            for l in links:
                release_url = "%s/%s" % (latest_url, l.attrib['href'])
                print('Fetching %s' % release_url)
                r = requests.get(release_url)
                data = r.json()
                writeReleases(data['releases'], 'all', data, release_url)
        else:
            print('Latest URL does not contain extensions - check page')
    else:
        url = '%s/merged_with_extensions_2017-06-23/release-0000001.json' \
            % BASE
        r = requests.get(url)
        data = r.json()
        writeReleases(data['releases'], 'sample', data, url)


if __name__ == '__main__':
    main()
