import json
import optparse
import os
from collections import defaultdict

import ocdsmerge
import requests
from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    parser.add_option(
        '-R', '--resume', action='store_true', default=False,
        help='Continue from the last page (in page.n)')
    parser.add_option('-p', '--page', action='store', type="int", default=1,
                      help='Start from page n of the results')
    parser.add_option('-c', '--compiled', action='store_true', default=False,
                      help='Merge the releases by ocid in compiledRelease and save it')

    (options, args) = parser.parse_args()

    if options.resume:
        with open("page.n", 'r') as n:
            page = n.read()
    else:
        page = options.page

    base_folder = os.path.dirname(os.path.realpath(__file__))
    folder = base_folder

    BASE = 'https://www.contractsfinder.service.gov.uk'
    url = '%s/Published/Notices/OCDS/Search?order=asc&page=%s' % (BASE, 1)
    if options.all:
        folder += '/all'

        r = requests.get(url)
        data = r.json()
        num_pages = data['maxPage']
        releases_by_ocid = defaultdict(list)
        print('%s pages to retrieve' % num_pages)
        for i in range(page, num_pages + 1):
            url = '%s/Published/Notices/OCDS/Search?order=asc&page=%s' % \
                (BASE, i)
            print('fetching %s' % url)
            data = common.getUrlAndRetry(url, folder)
            if data is None:
                continue
            for r in data['results']:
                    common.writeReleases(r['releases'], folder, r, url)

            with open("page.n", 'w') as n:
                n.write(str(i))
        with open("page.n", 'w') as n:
            n.write("1")
        if options.compiled:
            folder += '/releases'
            json_files = [x for x in os.listdir(folder) if x.endswith("json")]
            for json_file in json_files:
                json_file_path = os.path.join(folder, json_file)
                with open(json_file_path, "r") as f:
                    release = json.load(f)
                    releases_by_ocid[release['ocid']].append(release)

            for ocid in releases_by_ocid:
                if len(releases_by_ocid[ocid]) > 1:
                    print('compiling ocid %s with %d releases' % (ocid, len(releases_by_ocid[ocid])))
                    compiled_release = ocdsmerge.merge(releases_by_ocid[ocid])
                    common.writeFile(ocid+'.json', base_folder+'/compiled', compiled_release, None)
                else:
                    common.writeFile(ocid + '.json', base_folder+'/compiled', releases_by_ocid[ocid][0], None)

    else:
        folder += '/sample'
        print('fetching %s' % url)
        data = common.getUrlAndRetry(url, folder)
        for r in data['results'][:10]:
            common.writeReleases(r['releases'], folder, r, url)


if __name__ == '__main__':
    main()
