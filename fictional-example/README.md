# Fictional example

## Maintenance

You will need [OCDS Kit](https://pypi.org/project/ocdskit/) and [jq](https://stedolan.github.io/jq/).

Update the tags in `tests/test_fictional_example.py`.

### 1.0

The release packages in the 1.0 directory are hand-written. After editing the release packages, create the record packages:

```shell
cat fictional-example/1.0/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.0/record/ocds-213czf-000-00001.json --schema https://standard.open-contracting.org/schema/1__0__3/release-schema.json > fictional-example/1.0/record/ocds-213czf-000-00001.json
cat fictional-example/1.0/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --versioned --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.0/record/ocds-213czf-000-00001-withversions.json --schema https://standard.open-contracting.org/schema/1__0__3/release-schema.json > fictional-example/1.0/record/ocds-213czf-000-00001-withversions.json
```

### 1.1

The release packages were generated from the [OCDS 1.1 Sample Data Spreadsheet Input Template](https://docs.google.com/spreadsheets/d/1P-q5S8-WUxYT6t8uVuZDvnGfsl39DhhZV_GvgR1GKHk/edit#gid=159397949).

1. Edit the template, as desired
1. Do steps 4 and 5 on the "Instructions" sheet
1. Save the JSON file to `fictional-example/1.1/ocds-213czf-000-00001.json`
1. Run `ocdskit indent fictional-example/1.1/ocds-213czf-000-00001.json`
1. Create the record packages:

        cat fictional-example/1.1/ocds-213czf-000-00001.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.1/record/ocds-213czf-000-00001.json > fictional-example/1.1/record/ocds-213czf-000-00001.json
        cat fictional-example/1.1/ocds-213czf-000-00001.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --versioned --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.1/record/ocds-213czf-000-00001-withversions.json > fictional-example/1.1/record/ocds-213czf-000-00001-withversions.json

1. Split the JSON file into many files, for easier browsing:

        cat fictional-example/1.1/ocds-213czf-000-00001.json | jq -crM | ocdskit split-release-packages 1 | split -l 1 -a 1 - fictional-example/1.1/ocds-213czf-000-00001-0

1. Rename the JSON files:

        mv fictional-example/1.1/ocds-213czf-000-00001-0a fictional-example/1.1/ocds-213czf-000-00001-01-planning.json
        mv fictional-example/1.1/ocds-213czf-000-00001-0b fictional-example/1.1/ocds-213czf-000-00001-02-tender.json
        mv fictional-example/1.1/ocds-213czf-000-00001-0c fictional-example/1.1/ocds-213czf-000-00001-03-tenderAmendment.json
        mv fictional-example/1.1/ocds-213czf-000-00001-0d fictional-example/1.1/ocds-213czf-000-00001-04-award.json
        mv fictional-example/1.1/ocds-213czf-000-00001-0e fictional-example/1.1/ocds-213czf-000-00001-05-contract.json
        mv fictional-example/1.1/ocds-213czf-000-00001-0f fictional-example/1.1/ocds-213czf-000-00001-06-implementation.json

Note that the [OCDS Data Review Tool](https://standard.open-contracting.org/review/) "loading some sample data" link refers to `ocds-213czf-000-00001-02-tender.json` above.
