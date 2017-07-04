import optparse
import os

from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'https://api.colombiacompra.gov.co/releases/'
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        folder += '/all'
        next_url = url
        while next_url:
            print('fetching %s' % next_url)
            data = common.getUrlAndRetry(next_url, folder)
            common.writeReleases(
                data['releases'], folder, data, next_url)
            next_url = data['links']['next']
    else:
        folder += '/sample'
        print('fetching %s' % url)
        data = common.getUrlAndRetry(url, folder)
        common.writeReleases(
            data['releases'], folder, data, url)


if __name__ == '__main__':
    main()
