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
            page = int(n.read())
    else:
        page = options.page

    tags = ['planning', 'tender', 'award', 'contract']
    for tag in tags:
        folder = os.path.dirname(os.path.realpath(__file__))
        base = 'http://gpp.ppda.go.ug'
        url = '%s/api/v1/releases?tag=%s&page=%s' % (base, tag, 1)
        if options.all:
            folder += '/all/' + tag
            r = requests.get(url)
            data = r.json()
            num_pages = data['pagination']['last_page']
            print('%s pages to retrieve' % num_pages)
            for i in range(page, num_pages + 1):
                url = '%s/api/v1/releases?tag=%s&page=%s' % \
                    (base, tag, i)
                print('fetching %s' % url)
                data = common.getUrlAndRetry(url, folder)
                if data is None:
                    continue
                for r in data['releases']:
                    common.writeReleases([r], folder, data, url)
                with open("page.n", 'w') as n:
                    n.write(str(i))
            with open("page.n", 'w') as n:
                n.write("1")
        else:
            folder += '/sample/' + tag
            print('fetching %s' % url)
            data = common.getUrlAndRetry(url, folder)
            for r in data['releases'][:10]:
                common.writeReleases([r], folder, data, url)


if __name__ == '__main__':
    main()
