import json
import os
from copy import deepcopy
from glob import glob
from collections import OrderedDict

import ocdsmerge


def merge(directory):
    releases = []
    packages = []
    linked_releases = []

    for filename in sorted(glob(os.path.join(directory, '*.json'))):
        with open(filename) as f:
            package = json.load(f)

        version = package.get('version')
        ocid = package['releases'][0]['ocid']

        for release in package['releases']:
            releases.append(release)
            packages.append(package['uri'] + '#' + release['id'])
            linked_releases.append(OrderedDict([
                ('url', package['uri'] + '#' + release['id']),
                ('date', release['date']),
                ('tag', release['tag']),
            ]))

    compiled_release = ocdsmerge.merge(releases)
    versioned_release = ocdsmerge.merge_versioned(releases)

    url = 'https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/{}/record/ocds-213czf-000-00001{{}}.json'  # noqa
    if version:
        infix = version
    else:
        infix = '1.0'

    template = OrderedDict([
        ('uri', url.format(infix)),
        ('publisher', package['publisher']),
        ('publishedDate', '2014-02-02T13:02:00Z'),
        ('packages', packages),
        ('records', [OrderedDict([
            ('ocid', ocid),
            ('releases', linked_releases),
            ('compiledRelease', compiled_release),
        ])]),
    ])

    if version:
        template['version'] = version
        template['extensions'] = []

    without_versioned = deepcopy(template)
    without_versioned['uri'] = template['uri'].format('')
    # No versioned release.

    with_versioned = deepcopy(template)
    with_versioned['uri'] = template['uri'].format('-withversions')
    with_versioned['records'][0]['versionedRelease'] = versioned_release

    return ocid, without_versioned, with_versioned


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    for minor_version in ('1.0', '1.1'):
        ocid, without_versioned, with_versioned = merge(os.path.join(path, minor_version))

        with open(os.path.join(path, minor_version, 'record', '{}.json'.format(ocid)), 'w') as f:
            json.dump(without_versioned, f, ensure_ascii=False, indent=2, separators=(',', ': '))
            f.write('\n')

        with open(os.path.join(path, minor_version, 'record', '{}-withversions.json'.format(ocid)), 'w') as f:
            json.dump(with_versioned, f, ensure_ascii=False, indent=2, separators=(',', ': '))
            f.write('\n')
