import json
import os
import warnings
from glob import glob

import requests
from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator as validator


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
