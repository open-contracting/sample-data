import optparse
import os

from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'https://armeps.am/ocds/release'
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        packages = 0
        folder += '/all'
        next_url = url
        while next_url:
            print('fetching', next_url)
            data = common.getUrlAndRetry(next_url, folder)
            common.writeFile('%s.json' % str(packages), folder, data, next_url)
            if 'next_page' in data:
                next_url = data['next_page']['uri']
            else:
                next_url = None
            packages = packages + 1
    else:
        folder += '/sample'
        next_url = url
        releases = 0
        while next_url and releases < 10:
            print('fetching', next_url)
            data = common.getUrlAndRetry(next_url, folder)
            common.writeFile('%s.json' % str(releases), folder, data, next_url)
            if 'next_page' in data:
                next_url = data['next_page']['uri']
            else:
                next_url = None
            releases = releases + 1


if __name__ == '__main__':
    main()
