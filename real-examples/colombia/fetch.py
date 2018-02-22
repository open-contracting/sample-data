import optparse
import os

from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    parser.add_option('-p', '--page', type="int", default=1,
                      help='Fetch records from the given page')
    parser.add_option(
        '-R', '--resume', action='store_true', default=False,
        help='Continue from the last page (in page.n)')
    parser.add_option('-b', '--bigquery', action='store_true', default=False,
                      help='Fetch records in bigquery format')

    (options, args) = parser.parse_args()

    if options.resume:
        with open("page.n", 'r') as n:
            page = int(n.read())
    else:
        page = options.page

    url = 'https://api.colombiacompra.gov.co/releases/?page=' + str(page)
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        folder += '/all'
        packages = 1
        next_url = url
        while next_url:
            print('fetching %s' % next_url)
            data = common.getUrlAndRetry(next_url, folder)
            if data is None:
                current_page = int(next_url.split('page=')[1])
                next_url = next_url.replace('page='+str(current_page), 'page='+str(current_page+1))
                continue
            if options.bigquery:
                common.writeReleases(
                    data['releases'], folder, data, next_url)
            else:
                common.writeFile('%s.json' % str(packages), folder, data, next_url)
            next_url = data['links']['next']
            with open("page.n", 'w') as n:
                n.write(str(packages))
            packages = packages + 1
    else:
        folder += '/sample'
        print('fetching %s' % url)
        data = common.getUrlAndRetry(url, folder)
        common.writeReleases(
            data['releases'], folder, data, url)


if __name__ == '__main__':
    main()
