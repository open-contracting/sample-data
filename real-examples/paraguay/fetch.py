import csv
import json
import optparse
from io import open

import requests
import requests_cache
from ratelimit import *


def writeFile(fname, r, url):
    try:
        with open(fname, 'w', encoding='utf8') as f:
            f.write(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        with open("errors.txt", 'a') as err:
            print("Failed to write %s, %s" % (fname, e))
            err.write(
                "Failed to write %s, %s, %s\n" % (fname, e, url))


def updateReleaseUrl(url):
    '''
    Paraguay's records contain incorrect release URLs - fix them.
    '''
    url = url.replace('/datos/id/', '/datos/api/v2/doc/ocds/')\
             .replace('.json', '')
    return url


@rate_limited(3)
def fetchRelease(folder, url):
    '''
    Given a release URL, save it locally.
    '''
    print("Fetching release: %s" % url)
    r = requests.get(url)
    d = url.split('/')
    # Filenames don't match IDs, as they should - fix them here.
    fname = '%s-%s' % (d[-1], d[-2])
    writeFile('%s/releases/%s.json' % (folder, fname), r, url)


@rate_limited(3)
def fetchRecords(id_list, folder, get_releases, page=0):
    '''
    Given a record ID, construct the package URL and save locally.
    '''
    record_id = id_list[page]
    url = 'https://www.contrataciones.gov.py:443/'
    url += 'datos/api/v2/doc/ocds/record-package/%s' % record_id
    print("Fetching record %s ID: %s > %s" % (page, record_id, url))
    r = requests.get(url)
    writeFile('%s/records/%s.json' % (folder, record_id), r, url)
    if get_releases:
        try:
            data = r.json()
            releases = data['packages']
            for url in releases:
                release_url = updateReleaseUrl(url)
                fetchRelease(folder, release_url)
        except Exception as e:
            with open("errors.txt", 'a') as err:
                print("Failed to get releases for record %s, %s" %
                      (record_id, e))
                err.write(
                    "Failed to get releases for record %s, %s, %s\n" %
                    (record_id, e, url))
    # Write a record of the current page.
    page += 1
    with open("page.n", 'w') as n:
        n.write(str(page))
    if page < len(id_list):
        fetchRecords(id_list, folder, get_releases, page)
    else:
        with open("page.n", 'w') as n:
            n.write(str("0"))


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
    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    # decoded_content = r.content.decode('utf-8').encode('utf-8')
    # reader = csv.DictReader(r.content.splitlines())
    id_list = []
    next(cr, None)
    # cr.next()
    for row in cr:
        id_list.append(row[2])
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
    parser.add_option('-r', '--releases', action='store_true',
                      default=False, help='Fetch releases as well as records')
    (options, args) = parser.parse_args()
    id_list = fetchList(options.year)
    # id_list = [273637, 273638, 273639]
    page = 0
    if options.resume:
        with open("page.n", 'r') as n:
            page = int(n.read())
    if options.all:
        fetchRecords(id_list, 'all', options.releases, page)
    else:
        id_list = id_list[:15]
        fetchRecords(id_list, 'sample', options.releases, page)

if __name__ == '__main__':
    main()
