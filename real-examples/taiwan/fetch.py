import optparse
import os

import requests

from common import common


def fetchReleases(data, folder, url):
    print('Fetching %s' % url)
    for r in data['releases']:
        # These releases are lacking IDs - set the ID to the OCID
        # (which is unique).
        r['id'] = r['ocid']
    common.writeReleases(data['releases'], folder, data, url)


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'http://data.dsp.im/dataset/963c0c3d-49ac-4a66-b8fa-f56c8166bb91/'
    url += 'resource/0abbe767-c940-49fe-80d3-bd68268f508e'
    url += '/download/2014-02.json'
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        r = requests.get(url)
        data = r.json()
        fetchReleases(data, '%s/all' % folder, url)
    else:
        r = requests.get(url)
        data = r.json()
        fetchReleases(data, '%s/sample' % folder, url)


if __name__ == '__main__':
    main()
