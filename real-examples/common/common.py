import json
import os
import time
from json import JSONDecodeError

import requests


def writeFile(fname, folder, data, url, filetype='releases'):
    if not os.path.exists(folder + '/'+filetype+'/'):
        os.makedirs(folder + '/'+filetype+'/')
    try:
        with open('%s/%s/%s' % (folder, filetype, fname),
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
    if 'license' in data:
        packageInfo['license'] = data['license']
    if 'publicationPolicy' in data:
        packageInfo['publicationPolicy'] = data['publicationPolicy']
    return packageInfo


def writeReleases(releases, folder, data, url, filetype='releases',  compiled=False, releases_by_ocid=None):
    '''
    Given a list of releases and some package information,
    extract each release and write it to a file,
    adding package information to the `packageInfo` property.

    Note: can also be used to write records (function needs renaming)
    '''
    packageInfo = extractPackageInfo(data)
    for i, r in enumerate(releases):
        if packageInfo:
            r['packageInfo'] = packageInfo
        else:
            r['packageInfo'] = None
        if compiled and releases_by_ocid is not None:
            releases_by_ocid[r['ocid']].append(r)
            continue
        # Filenames are a combination of the release OCID and ID,
        # which should guarantee uniqueness.
        # Replace characters (e.g. in timestamps) that cause problems.
        fname = '%s-%s.json' % (
            r['ocid'].replace('/', ''),
            r['id'].replace(':', '_').replace('.', '_').replace('/', ''))
        writeFile(fname, folder, r, url, filetype)
        if folder.endswith('sample') and i >= 10:
            break
    return releases


def getUrlAndRetry(url, folder, isJson=True, tries=1, requestHeader=None):
    '''
    Handle transient network errors, and URLs with
    intermittent timeouts.
    '''
    if tries > 10:
        err = 'Too many retries, giving up: %s' % url
        print(err)
        with open('%s/errors.txt' % folder, 'a') as errors:
            errors.write(err)
        return None
    try:

        r = requests.get(url, headers=requestHeader)
    except requests.exceptions.Timeout:
        print('Request timeout (attempt %s), retrying %s' % (tries, url))
        time.sleep(10)
        return getUrlAndRetry(url, folder, isJson, tries + 1)
    except requests.ConnectionError:
        print('Connection error (attempt %s), retrying %s' % (tries, url))
        time.sleep(10)
        return getUrlAndRetry(url, folder, isJson, tries + 1)
    except requests.exceptions.TooManyRedirects:
        err = 'Too many redirects, giving up: %s' % url
        print(err)
        with open('%s/errors.txt' % folder, 'a') as errors:
            errors.write(err)
        return None
    except requests.exceptions.RequestException as e:
        err = 'Request exception %s, giving up: %s' % (e, url)
        print(err)
        with open('%s/errors.txt' % folder, 'a') as errors:
            errors.write(err)
        return None
    if not r.ok:
        print('Not ok response (attempt %s), retrying %s' % (tries, url))
        time.sleep(1)
        return getUrlAndRetry(url, folder, isJson, tries + 1)
    if isJson:
        try:
            return r.json()
        except JSONDecodeError:
            return getUrlAndRetry(url, folder, isJson, tries + 1)
    else:
        return r
