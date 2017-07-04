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
    url = 'http://www.contratosabiertos.cdmx.gob.mx/api/contratos/todos'
    r = requests.get(url)
    data = r.json()
    package_urls = [d['uri'] for d in data]
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        folder += '/all'
    else:
        folder += '/sample'
        package_urls = package_urls[:4]
    for url in package_urls:
        print('fetching', url)
        data = common.getUrlAndRetry(url, folder)
        common.writeReleases(data['releases'], folder, data, url)


if __name__ == '__main__':
    main()
