#!/bin/bash
set -e # exit on error

curl -s -S -O "http://standard.open-contracting.org/schema/1__0__3/release-package-schema.json"
curl -s -S -O "http://standard.open-contracting.org/schema/1__0__3/record-package-schema.json"
curl -s -S -O "http://standard.open-contracting.org/schema/1__0__3/release-schema.json"
cd fictional-example/1.0
# Check that files validate
for f in *.json; do echo $f; jsonschema ../../release-package-schema.json -i  $f; done
# Check that running merge.py produces the same output as what's curently in
# the repo
cp record/ocds-213czf-000-00001.json record/ocds-213czf-000-00001.json.OLD && python merge.py && diff record/ocds-213czf-000-00001.json.OLD record/ocds-213czf-000-00001.json
# Clean up after ourselves
cd ../../
rm *.json*
