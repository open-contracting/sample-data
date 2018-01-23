import optparse
import os

from common import common
from lxml import html


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    parser.add_option('-b', '--bigquery', action='store_true', default=False,
                      help='Fetch records in bigquery format')
    (options, args) = parser.parse_args()
    count = 0
    services = ['rftproposed.list', 'RFT.list', 'RFT.closed', 'RFT.archived']
    rft_uuids = []
    folder = os.path.dirname(os.path.realpath(__file__))
    if not options.all:
        url = 'https://tenders.nsw.gov.au'
        url += '/?event=public.%s&ResultsPerPage=%s'
        data = common.getUrlAndRetry(url % ('RFT.list', '10'), folder, isJson=False)
        rft_uuids = rft_uuids + (html.fromstring(data.content).xpath(
            '//div[@class="list-box"]/div/div[@class="row"]/div[@class="col-sm-8 col-md-9"]/div[@class="row"]/div['
            '@class="col-sm-10"]/h2/a/@href'))
        folder += '/sample'

    else:
        folder += '/all'
        for service in services:
            url = 'https://tenders.nsw.gov.au'
            url += '/?event=public.%s&ResultsPerPage=%s'
            url = url % (service, '20000')
            print('fetching', url)
            data = common.getUrlAndRetry(url, folder, isJson=False)
            rft_uuids = rft_uuids + (html.fromstring(data.content).xpath(
                '//div[@class="list-box"]/div/div[@class="row"]/div[@class="col-sm-8 col-md-9"]/div[@class="row"]/div['
                '@class="col-sm-10"]/h2/a/@href'))

    rft_uuids = set(rft_uuids)
    print('%s rftuuids in total' % len(rft_uuids))
    tender_url = 'https://tenders.nsw.gov.au/?event=public.api.tender.view&RFTUUID=%s'
    for next_url in rft_uuids:
        complete_url = tender_url % next_url.split('RFTUUID=')[1]
        print('fetching', complete_url)
        data = common.getUrlAndRetry(complete_url, folder)
        if options.bigquery:
            common.writeReleases(
                data['releases'], folder, data, next_url)
        else:
            common.writeFile('%s.json' % count, folder, data, next_url)
        count = count + 1


if __name__ == '__main__':
    main()
