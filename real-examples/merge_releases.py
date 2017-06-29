import glob
import json
import optparse
from pprint import pprint

import ocdsmerge

'''
For publishers that publish releases, but not records.
Combine releases that share an OCID into records.
'''


def mergeReleases(releases):
    record = {}
    # TODO: Clarify what to do about packages, publishedData,
    # publisher and uri fields for the record.
    record['compiledRelease'] = ocdsmerge.merge(releases)
    record['versionedRelease'] = ocdsmerge.merge_versioned(releases)
    record['releases'] = releases
    if 'publisher' in releases[0]:
        record['publisher'] = releases[0]['publisher']
    elif 'packageInfo' in releases[0]:
        record['publisher'] = releases[0]['packageInfo']['publisher']
    return record


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option(
        '-f', '--filepath', action='store', default=None,
        help='Path to release files, e.g. paraguay/sample/releases')
    parser.add_option(
        '-o', '--outfilepath', action='store', default=None,
        help='Path to release files, e.g. paraguay/sample/releases')
    (options, args) = parser.parse_args()
    if not options.filepath:
        parser.error(
            'You must supply an input filepath, using the -f argument')
    if not options.outfilepath:
        parser.error(
            'You must supply a destination filepath, using the -o argument')
    ocids = {}
    for filename in glob.glob('%s/*.json' % options.filepath):
        if not filename.endswith('.json'):
            print('Skipping non-JSON file %s' % filename)
            continue
        with open(filename, 'r') as file:
            release = json.loads(file.read())
            ocid = release['ocid']
            if ocid not in ocids:
                ocids[ocid] = [release]
            else:
                ocids[ocid].append(release)
    for ocid in ocids:
        record = mergeReleases(ocids[ocid])
        fname = '%s/%s.json' % (options.outfilepath, ocid.replace('/', '_'))
        with open(fname, 'w') as writefile:
            writefile.write(json.dumps(record, indent=2))

if __name__ == '__main__':
    main()
