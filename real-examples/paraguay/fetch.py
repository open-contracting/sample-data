import csv
import json
import optparse
from io import open

import requests
import requests_cache
from ratelimit import *


@rate_limited(3)
def fetchData(id_list, folder, page=0):
    '''
    Given a record ID, write it to JSON.
    '''
    record_id = id_list[page]
    url = 'https://www.contrataciones.gov.py:443/'
    url += 'datos/api/v2/doc/ocds/record-package/%s' % record_id
    print("Fetching record %s ID: %s > %s" % (page, record_id, url))
    r = requests.get(url)
    try:
        # print(r.json())
        fname = '%s/%s.json' % (folder, record_id)
        print(fname)
        with open(fname, 'w', encoding='utf8') as release:
            release.write(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        with open("errors.txt", 'a') as err:
            print("Failed to write %s, %s" % (record_id, e))
            err.write(unicode(url))
    # Write a record of the current page.
    page += 1
    with open("page.n", 'w') as n:
        n.write(unicode(str(page)))
    if page < len(id_list):
        fetchData(id_list, folder, page)
    else:
        with open("page.n", 'w') as n:
            n.write(unicode("0"))


@rate_limited(1)
def fetchList(year):
    '''
    Download the CSV file for a particular year, and
    extract the list of record IDs.
    '''
    url = 'https://www.contrataciones.gov.py/'
    url += 'images/opendata/planificaciones/%s.csv' % year
    print("Fetching %s listing, from %s" % (year, url))
    r = requests.get(url)
    decoded_content = r.content.decode('utf-8').encode('utf-8')
    reader = csv.DictReader(decoded_content.splitlines())
    id_list = []
    for row in reader:
        id_list.append(row['id_llamado'])
    return id_list


def main():
    requests_cache.install_cache('test_cache', backend='sqlite',
                                 expire_after=300)
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    parser.add_option('-R', '--resume', action='store_true', default=False,
                      help='Continue from the last page (in page.n), for when \
                      download broken')
    parser.add_option('-y', '--year', action='store', type="int", default=2016,
                      help='Which year to fetch activities from')
    (options, args) = parser.parse_args()
    id_list = fetchList(options.year)
    # id_list = [273637, 273638, 273639]
    page = 0
    if options.resume:
        with open("page.n", 'r') as n:
            page = int(n.read())
    if options.all:
        fetchData(id_list, 'all', page)
    else:
        id_list = id_list[:50]
        fetchData(id_list, 'sample', page)

if __name__ == '__main__':
    main()
