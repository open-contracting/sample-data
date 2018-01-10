import http.client
import json
import optparse
import os
import urllib
import zipfile
from urllib.request import urlopen

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
                temp = resource['url'].split("//")[1]
                conn = http.client.HTTPConnection(temp.split("/")[0])
                conn.request('HEAD', "/"+temp.split("/")[1])
                response = conn.getresponse()
                url = response.getheader('Location').replace("open?", "uc?export=download&")
                urls.append(url)
    return urls


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'http://datos.gob.mx/busca/api/3/action/'
    url += 'package_search?q=organization:contrataciones-abiertas&rows=500'
    folder = os.path.dirname(os.path.realpath(__file__))
    release_packages = getReleasePackages(url)
    if options.all:
        folder += '/all'
    else:
        folder += '/sample'
    for url in release_packages:
        print('fetching %s' % url)
        urllib.request.urlretrieve(url, "file.zip")
        with zipfile.ZipFile("file.zip", "r") as zip_ref:
            zip_ref.extractall(os.getcwd())
            zip_ref.close()
        with open(os.getcwd()+'/contratacionesabiertas_bulk.json') as data_file:
            data = json.load(data_file, encoding='latin1')
            if not options.all:
                data = data[:10]
            if type(data) == list:
                for d in data:
                    common.writeReleases(
                        [d['records'][0]['compiledRelease']], folder, d, url, 'records')
            else:
                common.writeReleases(
                    data['releases'], folder, data, url)
            data_file.close()
        break

if __name__ == '__main__':
    main()
