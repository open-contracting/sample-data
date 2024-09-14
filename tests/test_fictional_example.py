import json
import os
import warnings
from glob import glob

import pytest
import requests
from jsonschema import FormatChecker
from jsonschema.validators import Draft4Validator as Validator
from referencing import Registry, Resource


def custom_warning_formatter(message, category, filename, lineno, line=None):
    return str(message).replace(os.getcwd() + os.sep, '')


warnings.formatwarning = custom_warning_formatter


def get_test_cases():
    test_valid_argvalues = []

    versions = {
        '1.0': '1__0__3',
        '1.1': '1__1__5',
    }

    url_template = 'https://standard.open-contracting.org/schema/{}/release-package-schema.json'

    for minor_version, patch_version in versions.items():
        package_schema_url = url_template.format(patch_version)
        package_schema = requests.get(package_schema_url).json()

        release_schema_url = package_schema_url.replace('-package', '')
        release_schema = requests.get(release_schema_url).json()

        registry = Registry().with_resource(release_schema_url, Resource.from_contents(release_schema))

        filenames = glob(os.path.join('fictional-example', minor_version, '*.json'))
        assert len(filenames), f'{minor_version} fixtures not found'
        test_valid_argvalues += [(filename, registry, package_schema) for filename in filenames]

    return test_valid_argvalues


@pytest.mark.parametrize(('filename', 'registry', 'schema'), get_test_cases())
def test_valid(filename, registry, schema):
    errors = 0

    with open(filename) as f:
        data = json.load(f)

    for error in Validator(schema, format_checker=FormatChecker(), registry=registry).iter_errors(data):
        errors += 1
        warnings.warn(json.dumps(error.instance, indent=2))
        warnings.warn(f"{error.message} ({'/'.join(error.absolute_schema_path)})\n")

    assert errors == 0, f'{filename} is invalid. See warnings below.'
