import json
import optparse
import os

import requests

from common import common


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
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        folder += '/all'
        url = '%s/multiple-file-api/releases.json' % BASE
        year_urls = fetchYears(url)
        for url in year_urls:
            print('fetching %s' % url)
            data = common.getUrlAndRetry(url, folder)
            common.writeReleases(data['releases'], folder, data, url)
    else:
        folder += '/all'
        url = '%s/ocds-api/year/2017' % BASE
        print('fetching %s' % url)
        data = common.getUrlAndRetry(url, folder)
        common.writeReleases(data['releases'], folder, data, url)

if __name__ == '__main__':
    main()
