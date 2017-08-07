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
    url = 'http://nigeriaoc.org/downloadSelected'
    r = requests.get(url)
    data = r.json()
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        folder += '/all'
    else:
        folder += '/sample'
    data = common.getUrlAndRetry(url, folder)
    common.writeReleases(data['releases'], folder, data, url)


if __name__ == '__main__':
    main()
