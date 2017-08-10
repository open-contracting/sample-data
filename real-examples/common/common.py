import json
import os
import time

import requests


def writeFile(fname, folder, data, url):
    if not os.path.exists(folder + '/releases/'):
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
    return releases


def getUrlAndRetry(url, folder, isJson=True, tries=1):
    '''
    Handle transient network errors, and URLs with
    intermittent timeouts.
    '''
    if tries > 10:
        err = 'Too many retries, giving up: %s' % url
        print(err)
        with open('%s/errors.txt' % folder, 'a') as err:
            err.write(err)
        return None
    try:
        r = requests.get(url)
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
        with open('%s/errors.txt' % folder, 'a') as err:
            err.write(err)
        return None
    except requests.exceptions.RequestException as e:
        err = 'Request exception %s, giving up: %s' % (e, url)
        print(err)
        with open('%s/errors.txt' % folder, 'a') as err:
            err.write(err)
        return None
    if isJson:
        return r.json()
    else:
        return r
