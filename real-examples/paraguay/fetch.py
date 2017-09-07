import csv
import optparse
import os
from io import open

import requests

from common import common

REQUEST_TOKEN = "Basic ODhjYmYwOGEtMDcyMC00OGY1LWFhYWUtMWVkNzVkZmFiYzZiOjNjNjQxZGQ5LWNjN2UtNDI5ZC05NWRiLWI5ODNiNmYyMDY3NA=="


def getAccessToken():
    r = requests.post("https://www.contrataciones.gov.py:443/datos/api/oauth/token",
                      headers={"Authorization": REQUEST_TOKEN})
    return "Bearer " + r.json()['access_token']

# @rate_limited(0.3)
def fetchRecord(record_id, folder, get_releases, page=0):
    '''
    Given a record ID, construct the package URL and save locally.
    '''
    url = 'https://www.contrataciones.gov.py:443/'
    url += 'datos/api/v2/doc/ocds/record-package/%s' % record_id
    print("Fetching record %s ID: %s > %s" % (page, record_id, url))
    data = common.getUrlAndRetry(url, folder)
    if data:
        try:
            common.writeReleases(
                [data['records'][0]['compiledRelease']], folder, data, url)
            if get_releases and 'packages' in data:
                releases = data['packages']
                for url in releases:
                    # Rewrite the release URL - they are published
                    # in an incorrect format.
                    release_url = url\
                        .replace('/datos/id/', '/datos/api/v2/doc/ocds/')\
                        .replace('.json', '')
                    print('fetching %s' % release_url)
                    release_data = common.getUrlAndRetry(release_url, folder)
                    if release_data and 'releases' in release_data:
                        common.writeReleases(
                            release_data['releases'], folder,
                            release_data, release_url)
        except KeyError:
            err = 'No compiledReleases, skipping this one: %s \n' % url
            print(err)
            with open('%s/errors.txt' % folder, 'a') as errors:
                errors.write(err)


# @rate_limited(0.3)
def fetchRecordPackageIDs(year):
    '''
    Download the CSV file for a particular year, and
    extract the list of record package IDs.
    '''
    url = 'https://www.contrataciones.gov.py/'
    url += 'images/opendata/planificaciones/%s.csv' % year
    print("Fetching %s record package IDs, from %s" % (year, url))
    r = requests.get(url)
    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    id_list = []
    next(cr, None)
    for row in cr:
        id_list.append(row[2])
    return id_list[1:]


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    parser.add_option('-R', '--resume', action='store_true', default=False,
                      help='Continue from the last page (in page.n), for when \
                      download broken')
    parser.add_option('-y', '--year', action='store', type="int", default=2016,
                      help='Which year to fetch activities from')
    parser.add_option('-s', '--skip', action='store_true',
                      default=False,
                      help='Skip downloads if file already exists')
    parser.add_option('-r', '--releases', action='store_true',
                      default=False, help='Fetch individual releases')
    (options, args) = parser.parse_args()

    record_package_ids = []
    if options.all and not options.year:
        for year in range(2010, 2018):
            record_package_ids += fetchRecordPackageIDs(year)
    else:
        record_package_ids += fetchRecordPackageIDs(options.year)
    print('%s record packages to retrieve' % len(record_package_ids))
    # record_package_ids = [273637, 273638, 273639]

    page = 0
    folder = os.path.dirname(os.path.realpath(__file__))
    page_file = folder + "/page.n"
    if options.resume:
        with open(page_file, 'r') as n:
            page = int(n.read())

    if options.all:
        folder += '/all'
    else:
        folder += '/sample'
        record_package_ids = record_package_ids[:4]
    for record_id in record_package_ids[page:]:
        if options.skip:
            record_file = '%s/records/ocds-03ad3f-%s.json' % \
                (folder, record_id)
            print(record_file)
            if os.path.isfile(record_file):
                print('record exists, skipping %s' % record_file)
                page += 1
                continue
        fetchRecord(record_id, folder, options.releases, page)
        page += 1
        with open(page_file, 'w') as n:
            n.write(str(page))
    with open(page_file, 'w') as n:
        n.write(str('1'))


if __name__ == '__main__':
    main()
