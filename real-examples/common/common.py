import json
import os


def writeFile(fname, folder, data, url):
    if not os.path.exists(folder):
        os.makedirs(folder + '/releases/')
    try:
        with open('%s/releases/%s' % (folder, fname),
                  'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        with open('%s/errors.txt' % folder, 'a') as err:
            print("Failed to write %s, %s" % (fname, e))
            err.write(
                "Failed to write %s, %s, %s\n" % (fname, e, url))


def extractPackageInfo(data):
    packageInfo = {}
    if 'uri' in data:
        packageInfo['uri'] = data['uri']
    if 'publishedDate' in data:
        packageInfo['publishedDate'] = data['publishedDate']
    if 'publisher' in data:
        packageInfo['publisher'] = data['publisher']
    return packageInfo


def writeReleases(releases, folder, data, url):
    '''
    Given a list of releases and some package information,
    extract each release and write it to a file,
    adding package information to the `packageInfo` property.
    '''
    packageInfo = extractPackageInfo(data)
    for i, r in enumerate(releases):
        if packageInfo:
            r['packageInfo'] = packageInfo
        else:
            r['packageInfo'] = None
        # Filenames are a combination of the release OCID and ID,
        # which should guarantee uniqueness.
        # Replace characters (e.g. in timestamps) that cause problems.
        fname = '%s-%s.json' % (
            r['ocid'].replace('/', ''),
            r['id'].replace(':', '_').replace('.', '_').replace('/', ''))
        writeFile(fname, folder, r, url)
        if folder.endswith('sample') and i >= 10:
            break
