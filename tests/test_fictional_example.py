import json
import os
import warnings
from glob import glob

import pytest
import requests
from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator as validator

versions = {
    '1.0': '1__0__3',
    '1.1': '1__1__4',
}

url_template = 'https://standard.open-contracting.org/schema/{}/release-package-schema.json'

test_valid_argvalues = []
for minor_version, patch_version in versions.items():
    schema = requests.get(url_template.format(patch_version)).json()
    filenames = glob(os.path.join('fictional-example', minor_version, '*.json'))
    assert len(filenames), '{} fixtures not found'.format(minor_version)
    test_valid_argvalues += [(filename, schema) for filename in filenames]


def custom_warning_formatter(message, category, filename, lineno, line=None):
    return str(message).replace(os.getcwd() + os.sep, '')


warnings.formatwarning = custom_warning_formatter


@pytest.mark.parametrize('filename,schema', test_valid_argvalues)
def test_valid(filename, schema):
    errors = 0

    with open(filename) as f:
        data = json.load(f)

    for error in validator(schema, format_checker=FormatChecker()).iter_errors(data):
        errors += 1
        warnings.warn(json.dumps(error.instance, indent=2, separators=(',', ': ')))
        warnings.warn('{} ({})\n'.format(error.message, '/'.join(error.absolute_schema_path)))

    assert errors == 0, '{} is invalid. See warnings below.'.format(filename)
