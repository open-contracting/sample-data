import optparse
import os

from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'https://ville.montreal.qc.ca/vuesurlescontrats/api/releases.json'
    folder = os.path.dirname(os.path.realpath(__file__))
    more_releases = True
    if options.all:
        offset = 0
        while more_releases:
            next_url = url + '?limit=10000&offset=%s' % offset
            print('fetching %s' % next_url)
            data = common.getUrlAndRetry(next_url, folder)
            more_releases = len(common.writeReleases(
                data['releases'], '%s/all' % folder, data, next_url))
            offset += 10000
    else:
        url += '?limit=10'
        print('fetching %s' % url)
        data = common.getUrlAndRetry(url, folder)
        common.writeReleases(
            data['releases'], '%s/sample' % folder, data, url)

if __name__ == '__main__':
    main()
