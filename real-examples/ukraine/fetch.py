import optparse
import os

from pyquery import PyQuery as pq
import requests

from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    parser.add_option(
        '-R', '--resume', action='store_true', default=False,
        help='Continue from last page (in page.n) for when download broken')
    parser.add_option('-p', '--page', action='store', type="int", default=1,
                      help='Start from page n of the results')
    (options, args) = parser.parse_args()
    if options.resume:
        with open("page.n", 'r') as n:
            page = n.read()
    else:
        page = options.page
    BASE = 'http://ocds.prozorro.openprocurement.io'
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        folder += '/all'
        urls = []
        r = requests.get(BASE)
        d = pq(r.content)
        links = d('.container ol li a')
        latest_url = "%s/%s" % (BASE, links[-2].attrib['href'])
        if 'with_extensions' in latest_url:
            r = requests.get(latest_url)
            d = pq(r.content)
            links = d('.container ol li a')
            for l in links:
                release_url = "%s/%s" % (latest_url, l.attrib['href'])
                urls.append(release_url)
        else:
            print('Latest URL does not contain extensions - check page')
    else:
        folder += '/sample'
        urls = [
            '%s/merged_with_extensions_2017-06-23/release-0000001.json' % BASE
        ]
    print('%s release packages to fetch' % len(urls))
    for url in urls:
        package_num = int(url.split('-')[-1].replace('.json', ''))
        if package_num < page:
            continue
        print('fetching %s' % url)
        data = common.getUrlAndRetry(url, folder)
        common.writeReleases(
            data['releases'], folder, data, url)
        with open("page.n", 'w') as n:
            n.write(str(package_num))


if __name__ == '__main__':
    main()
