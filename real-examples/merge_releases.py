import glob
import json
import optparse
import os

import ocdsmerge

'''
For publishers that publish releases, but not records.
Combine releases that share an OCID into records,
then writes the records to files named by OCID.
'''


def mergeReleases(releases):
    record = {}
    # TODO: Clarify what to do about packages, publishedData,
    # and uri fields for the record.
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
        help='Path to record files, e.g. paraguay/sample/records')
    (options, args) = parser.parse_args()
    if not options.filepath:
        parser.error(
            'You must supply an input filepath, using the -f argument')
    if not options.outfilepath:
        parser.error(
            'You must supply a destination filepath, using the -o argument')
    if not os.path.exists(options.outfilepath):
        os.makedirs(options.outfilepath)
    ocids = {}
    files = glob.glob('%s/*.json' % options.filepath)
    for filename in files:
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
    print('Consolidating %s OCIDs' % len(ocids))
    count = 0
    for ocid in ocids:
        count += 1
        if not count % 1000:
            print('Merging OCID %s of %s' % (count, len(ocids)))
        record = mergeReleases(ocids[ocid])
        fname = '%s/%s.json' % (options.outfilepath, ocid.replace('/', '_'))
        with open(fname, 'w') as writefile:
            writefile.write(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
