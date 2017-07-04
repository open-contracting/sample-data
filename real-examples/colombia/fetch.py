import optparse
import os

from common import common


def writeFile(fname, data, url):
    try:
        with open(fname, 'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        with open("errors.txt", 'a') as err:
            print("Failed to write %s, %s" % (fname, e))
            err.write(
                "Failed to write %s, %s, %s\n" % (fname, e, url))


def fetchReleases(data, folder, url):
    print('Fetching %s' % url)
    for i, r in enumerate(data['releases']):
        # These release packages lack URIs and dates.
        r['packageInfo'] = {
            'uri': None,
            'publishedDate': None,
            'publisher': data['publisher']
        }
        fname = '%s/releases/%s-%s.json' % \
            (folder, r['ocid'].replace('/', '_'), r['id'].replace('/', '_'))
        print(fname)
        writeFile(fname, r, url)


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a', '--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')
    (options, args) = parser.parse_args()
    url = 'https://api.colombiacompra.gov.co/releases/'
    folder = os.path.dirname(os.path.realpath(__file__))
    if options.all:
        next_url = url
        while next_url:
            print('fetching %s' % next_url)
            data = common.getUrlAndRetry(next_url, folder)
            common.writeReleases(
                data['releases'], '%s/all' % folder, data, next_url)
            next_url = data['links']['next']
    else:
        print('fetching %s' % url)
        data = common.getUrlAndRetry(url, folder)
        common.writeReleases(
            data['releases'], '%s/sample' % folder, data, url)


if __name__ == '__main__':
    main()
