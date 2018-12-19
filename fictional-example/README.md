# Fictional example

## Maintenance

After editing the release packages, create the record packages. You will need [OCDS Kit]().

```
cat fictional-example/1.0/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.0/record/ocds-213czf-000-00001.json > fictional-example/1.0/record/ocds-213czf-000-00001.json
cat fictional-example/1.0/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --versioned --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.0/record/ocds-213czf-000-00001-withversions.json > fictional-example/1.0/record/ocds-213czf-000-00001-withversions.json
cat fictional-example/1.1/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.1/record/ocds-213czf-000-00001.json > fictional-example/1.1/record/ocds-213czf-000-00001.json
cat fictional-example/1.1/*.json | jq -crM | ocdskit --pretty compile --package --linked-releases --published-date 2014-02-02T13:02:00Z --versioned --uri https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.1/record/ocds-213czf-000-00001-withversions.json > fictional-example/1.1/record/ocds-213czf-000-00001-withversions.json
```
