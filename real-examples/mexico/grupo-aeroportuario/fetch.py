import json
import optparse

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
        fname = '%s/releases/%s-%s.json' % \
            (folder, r['ocid'],
             r['id'].replace('.', '_').replace(':', '_'))
        writeFile(fname, r, url)
        if folder == 'sample' and i >= 10:
            break


def getReleases(url, folder):
    print('fetching', url)
    r = requests.get(url)
    data = r.json()
    if folder == 'sample':
        for d in data[:10]:
            writeReleases(d['releases'], folder, d, url)
    else:
        if type(data) == list:
            writeReleases(d['releases'], folder, d, url)
        else:
            writeReleases(d['releases'], folder, d, url)


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'http://datos.gob.mx/busca/api/3/action/'
    url += 'package_search?q=organization:gacm&rows=500'
    r = requests.get(url)
    data = r.json()
    sources = []
    for result in data['result']['results']:
        for resource in result['resources']:
            if resource['format'] == 'JSON':
                sources.append(resource['url'])
    if options.all:
        for s in sources:
            getReleases(s, 'all')
    else:
        for s in sources[:1]:
            getReleases(s, 'sample')


if __name__ == '__main__':
    main()
