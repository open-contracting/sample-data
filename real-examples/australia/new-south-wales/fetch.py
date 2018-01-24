import optparse
import os

from common import common


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    parser.add_option('-b', '--bigquery', action='store_true', default=False,
                      help='Fetch records in bigquery format')
    (options, args) = parser.parse_args()
    url = 'https://tenders.nsw.gov.au'
    url += '/?event=public.api.%s.search&ResultsPerPage=50'
    folder = os.path.dirname(os.path.realpath(__file__))
    count = 0
    if options.all:
        folder += '/all'
        release_types = ['planning', 'tender', 'contract']
        for r in release_types:
            next_url = url % r
            while next_url:
                print('fetching', next_url)
                data = common.getUrlAndRetry(next_url, folder)

                for release in data['releases']:
                    stage_urls = []
                    if r == 'planning':
                        uuid = release['tender']['plannedProcurementUUID']
                        stage_urls.append('https://tenders.nsw.gov.au/?event=public.api.planning.view'
                                          '&PlannedProcurementUUID=%s' % uuid)
                        count = count + 1
                    if r == 'tender':
                        uuid = release['tender']['RFTUUID']
                        stage_urls.append('https://tenders.nsw.gov.au/?event=public.api.tender.view&RFTUUID=%s' % uuid)
                        count = count + 1
                    if r == 'contract':
                        for award in release['awards']:
                            uuid = award['CNUUID']
                            stage_urls.append('https://tenders.nsw.gov.au/?event=public.api.contract.view&CNUUID=%s' % uuid)
                            count = count + 1
                    for stage_url in stage_urls:
                        print('fetching', stage_url)
                        stage_data = common.getUrlAndRetry(stage_url, folder)
                        if options.bigquery:
                            common.writeReleases(
                                stage_data['releases'], folder, stage_data, stage_url)
                        else:
                            common.writeFile('%s-%s.json' % (r, count), folder, stage_data, stage_url)
                if 'next' in data['links']:
                    next_url = data['links']['next']
                else:
                    next_url = None
    else:
        folder += '/sample'
        next_url = url % 'planning'
        print('fetching', next_url)
        data = common.getUrlAndRetry(next_url, folder)
        if options.bigquery:
            common.writeReleases(
                data['releases'], folder, data, next_url)
        else:
            common.writeFile('%s.json' % count, folder, data, next_url)


if __name__ == '__main__':
    main()
