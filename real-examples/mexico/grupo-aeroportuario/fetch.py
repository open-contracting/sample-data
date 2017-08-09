import optparse
import os

import requests

from common import common


def getReleasePackages(url):
    '''
    This publisher publishes a list of links to release packages,
    in a custom format.
    Retrieve the URLs of all the release packages.
    '''
    r = requests.get(url)
    data = r.json()
    urls = []
    for result in data['result']['results']:
        for resource in result['resources']:
            if resource['format'] == 'JSON':
                urls.append(resource['url'])
    return urls


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'http://datos.gob.mx/busca/api/3/action/'
    url += 'package_search?q=organization:gacm&rows=500'
    folder = os.path.dirname(os.path.realpath(__file__))
    release_packages = getReleasePackages(url)
    if options.all:
        folder += '/all'
    else:
        release_packages = release_packages[:1]
        folder += '/sample'
    for url in release_packages:
        print('fetching %s' % url)
        data = common.getUrlAndRetry(url, folder)
        if type(data) == list:
            for d in data:
                common.writeReleases(d['releases'], folder, d, url)
        else:
            common.writeReleases(
                data['releases'], folder, data, url)

if __name__ == '__main__':
    main()
