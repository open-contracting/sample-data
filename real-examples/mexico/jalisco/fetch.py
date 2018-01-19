import optparse
import os

import requests

from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    parser.add_option('-b', '--bigquery', action='store_true', default=False,
                      help='Save the data in big query format')
    parser.add_option('-r', '--releases', action='store_true',
                      default=False, help='Fetch individual releases')
    (options, args) = parser.parse_args()
    url = 'https://contratacionesabiertas.jalisco.gob.mx/OCApi/2017/contracts'
    r = requests.get(url)
    data = r.json()
    package_urls = [d['URIContract'] for d in data]
    folder = os.path.dirname(os.path.realpath(__file__))
    count = 1
    if options.all:
        folder += '/all'
    else:
        folder += '/sample'
        package_urls = package_urls[:10]
    for url in package_urls:
        print('fetching', url)
        data_array = common.getUrlAndRetry(url, folder)
        for data in data_array:
            if options.bigquery:
                common.writeReleases(
                    [data['records'][0]['compiledRelease']], folder, data, url, 'records')
            else:
                common.writeFile('%s.json' % str(data['uri'].split('/')[-1]), folder, data, url, 'records')
            if options.releases:
                for release_url in data['packages']:
                    if count > 10 and not options.all:
                        break
                    print('fetching', release_url)
                    releases = common.getUrlAndRetry(release_url, folder)
                    for release in releases:
                        count = count + 1
                        if options.bigquery:
                            common.writeReleases(release['releases'], folder, release, release_url)
                        else:
                            common.writeFile('%s.json' % str(release_url.split('/')[-1]), folder, release, release_url)


if __name__ == '__main__':
    main()
