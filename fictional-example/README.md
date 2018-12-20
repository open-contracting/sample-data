# Fictional example

## Maintenance

You will need [OCDS Kit](https://pypi.org/project/ocdskit/) and [jq](https://stedolan.github.io/jq/).

### 1.0

The release packages in the 1.0 directory are hand-written. After editing the release packages, create the record packages:

```shell
cat fictional-example/1.0/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.0/record/ocds-213czf-000-00001.json > fictional-example/1.0/record/ocds-213czf-000-00001.json
cat fictional-example/1.0/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --versioned --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.0/record/ocds-213czf-000-00001-withversions.json > fictional-example/1.0/record/ocds-213czf-000-00001-withversions.json
```

### 1.1

The release packages were generated from the [OCDS 1.1 Sample Data Spreadsheet Input Template](https://docs.google.com/spreadsheets/d/1P-q5S8-WUxYT6t8uVuZDvnGfsl39DhhZV_GvgR1GKHk/edit#gid=159397949).

1. Edit the template, as desired
1. Do steps 4 and 5 on the "Instructions" sheet
1. Save the JSON file to `fictional-example/1.1/ocds-213czf-000-00001.json`
1. Run `ocdskit indent fictional-example/1.1/ocds-213czf-000-00001.json`
1. Create the record packages:

```shell
cat fictional-example/1.1/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.1/record/ocds-213czf-000-00001.json > fictional-example/1.1/record/ocds-213czf-000-00001.json
cat fictional-example/1.1/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --versioned --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.1/record/ocds-213czf-000-00001-withversions.json > fictional-example/1.1/record/ocds-213czf-000-00001-withversions.json
```
