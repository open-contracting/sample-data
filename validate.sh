#!/bin/bash
set -e # exit on error
wget "http://ocds.open-contracting.org/standard/r/1__0__0/release-package-schema.json"
cd fictional-example
for f in *.json; do echo $f; jsonschema ../release-package-schema.json -i  $f; done
