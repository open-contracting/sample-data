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


def fetchReleases(data, folder, url):
    print('Fetching %s' % url)
    unique_ocids = []
    for i, r in enumerate(data['releases']):
        r['packageInfo'] = {
            'uri': data['uri'],
            'publishedDate': data['publishedDate'],
            'publisher': data['publisher']
        }
        # Usually the filename would be the OCID plus the ID, but here
        # we just use the OCID, checking that OCIDs are unique.
        # Also set the release ID here, to get them through update process.
        if r['ocid'] in unique_ocids:
            print('DUPLICATE OCID: %s' % r['ocid'])
        else:
            unique_ocids.append(r['ocid'])
        r['id'] = r['ocid']
        fname = '%s/releases/%s.json' % \
            (folder, r['ocid'].replace('/', '_'))
        writeFile(fname, r, url)
        if folder == 'sample' and i >= 9:
            break


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'http://data.dsp.im/dataset/963c0c3d-49ac-4a66-b8fa-f56c8166bb91/'
    url += 'resource/0abbe767-c940-49fe-80d3-bd68268f508e'
    url += '/download/2014-02.json'
    if options.all:
        r = requests.get(url)
        data = r.json()
        fetchReleases(data, 'all', url)
    else:
        r = requests.get(url)
        data = r.json()
        fetchReleases(data, 'sample', url)

if __name__ == '__main__':
    main()
