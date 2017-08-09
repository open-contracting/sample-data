import optparse
import requests
import json


def writeFile(fname, data, url):
    try:
        with open(fname, 'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        with open("errors.txt", 'a') as err:
            print("Failed to write %s, %s" % (fname, e))
            err.write(
                "Failed to write %s, %s, %s\n" % (fname, e, url))


def writeReleases(page, folder, maxpage=0):
    BASE = 'https://www.contractsfinder.service.gov.uk'
    url = '%s/Published/Notices/OCDS/Search?order=asc&page=%s' % (BASE, page)
    print("Fetching page %s: %s" % (page, url))
    r = requests.get(url)
    data = r.json()
    try:
        if maxpage > -1:
            maxpage = data['maxPage']
        results = data['results']
        for i, result in enumerate(results):
            # TODO: Write records here, as well as results.
            for j, release in enumerate(results[i]['releases']):
                fname = folder + '/releases/' + \
                    result['releases'][j]['id'] + ".json"
                writeFile(fname, release, url)
                if folder == 'sample' and i >= 10:
                    return
    except:
        with open("errors.txt", 'a') as err:
            print("Failed to get " + str(page))
            err.write("%s\n" % url)
    # Keep track of which page has been reached.
    page = int(page) + 1
    with open("page.n", 'w') as n:
        n.write(str(page))
    if page <= maxpage or int(maxpage) == 0:
        fetchData(page, folder)
    else:
        with open("page.n", 'w') as n:
            n.write("1")


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
    if options.all:
        writeReleases(page, 'all')
    else:
        writeReleases(page, 'sample', -1)

if __name__ == '__main__':
    main()
