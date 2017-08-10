import optparse
import os

import requests

from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    parser.add_option(
        '-R', '--resume', action='store_true', default=False,
        help='Continue from the last page (in page.n)')
    parser.add_option('-p', '--page', action='store', type="int", default=1,
                      help='Start from page n of the results')

    (options, args) = parser.parse_args()

    if options.resume:
        with open("page.n", 'r') as n:
            page = n.read()
    else:
        page = options.page
    folder = os.path.dirname(os.path.realpath(__file__))

    BASE = 'https://www.contractsfinder.service.gov.uk'
    url = '%s/Published/Notices/OCDS/Search?order=asc&page=%s' % (BASE, 1)
    if options.all:
        folder += '/all'
        r = requests.get(url)
        data = r.json()
        num_pages = data['maxPage']
        print('%s pages to retrieve' % num_pages)
        for i in range(page, num_pages+1):
            url = '%s/Published/Notices/OCDS/Search?order=asc&page=%s' % \
                (BASE, i)
            print('fetching %s' % url)
            data = common.getUrlAndRetry(url, folder)
            for r in data['results']:
                common.writeReleases(r['releases'], folder, r, url)
            with open("page.n", 'w') as n:
                n.write(str(i))
        with open("page.n", 'w') as n:
            n.write("1")
    else:
        folder += '/sample'
        print('fetching %s' % url)
        data = common.getUrlAndRetry(url, folder)
        for r in data['results'][:10]:
            common.writeReleases(r['releases'], folder, r, url)

if __name__ == '__main__':
    main()
