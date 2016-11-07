#!/bin/bash
set -e # exit on error
wget "http://ocds.open-contracting.org/standard/r/1__0__1/release-package-schema.json"
wget "http://ocds.open-contracting.org/standard/r/1__0__1/release-schema.json"
cd fictional-example
# Check that files validate
for f in *.json; do echo $f; python ../jsonschema_with_formatchecker.py ../release-package-schema.json -i  $f; done
# Check that running merge.py produces the same output as what's curently in
# the repo
cp record/ocds-213czf-000-00001.json record/ocds-213czf-000-00001.json.OLD && python merge.py && diff record/ocds-213czf-000-00001.json.OLD record/ocds-213czf-000-00001.json
