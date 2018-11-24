import json
import os
import sys
import warnings
from glob import glob

import requests
from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator as validator

sys.path.append('fictional-example')

from merge import merge


patch_versions = {
    '1.0': '1__0__3',
    '1.1': '1__1__3',
}

cwd = os.getcwd()


def custom_warning_formatter(message, category, filename, lineno, line=None):
    return str(message).replace(cwd + os.sep, '')


warnings.formatwarning = custom_warning_formatter


def test_valid():
    errors = 0

    for minor_version in ('1.0', '1.1'):
        url = 'http://standard.open-contracting.org/schema/{}/release-package-schema.json'
        schema = requests.get(url.format(patch_versions[minor_version])).json()
        for filename in glob(os.path.join('fictional-example', minor_version, '*.json')):
            with open(filename) as f:
                data = json.load(f)
            for error in validator(schema, format_checker=FormatChecker()).iter_errors(data):
                errors += 1
                warnings.warn(json.dumps(error.instance, indent=2, separators=(',', ': ')))
                warnings.warn('{} ({})\n'.format(error.message, '/'.join(error.absolute_schema_path)))

    assert errors == 0, 'One or more JSON files are invalid. See warnings below.'


def test_merge():
    path = os.path.join('fictional-example')
    for minor_version in ('1.0', '1.1'):
        ocid, without_versioned, with_versioned = merge(os.path.join(path, minor_version))

        with open(os.path.join(path, minor_version, 'record', '{}.json'.format(ocid))) as f:
            actual = json.load(f)
        assert actual == without_versioned

        with open(os.path.join(path, minor_version, 'record', '{}-withversions.json'.format(ocid))) as f:
            actual = json.load(f)
        assert actual == with_versioned
