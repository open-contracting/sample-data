import optparse
import os

import requests

from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    BASE = 'https://buyandsell.gc.ca'
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        # No new data is being published, so just get the four
        # years that exist.
        urls = []
        for i in range(13, 17):
            url = '%s/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-%s-%s.json' \
                % (BASE, i, i+1)
            urls.append(url)
        for url in urls:
            print("Fetching releases for %s" % url)
            r = requests.get(url)
            data = r.json()
            common.writeReleases(
                data['releases'], '%s/all' % folder, data, url)
    else:
        url = '%s/cds/public/ocds/tpsgc-pwgsc_ocds_EF-FY-15-16.json' % BASE
        print("Fetching releases for %s" % url)
        r = requests.get(url)
        data = r.json()
        common.writeReleases(
            data['releases'], '%s/sample' % folder, data, url)

if __name__ == '__main__':
    main()
