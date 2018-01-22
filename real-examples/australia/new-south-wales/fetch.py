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
    url = 'https://tenders.nsw.gov.au'
    url += '/?event=public.RFT.list&ResultsPerPage=%s'
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        folder += '/all'
        url = url % '200'
    else:
        folder += '/sample'
        url = url % '10'
    tender_url = 'https://tenders.nsw.gov.au/?event=public.api.tender.view&RFTUUID=%s'

    count = 0
    data = common.getUrlAndRetry(url, folder, isJson=False)
    rft_uuids = (html.fromstring(data.content).xpath(
        '//div[@class="list-box"]/div/div[@class="row"]/div[@class="col-sm-8 col-md-9"]/div[@class="row"]/div['
        '@class="col-sm-10"]/h2/a/@href'))

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
