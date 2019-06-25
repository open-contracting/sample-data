# Flat Template

[Flatten Tool](https://flatten-tool.readthedocs.io/en/latest/usage-ocds/) can be used to convert to and from OCDS JSON and CSV or Excel.

This folder contains CSV and spreadsheet templates for OCDS 1.1.3, generated using Flatten Tool as described under Maintenance below.

## Using the CSV and Excel templates

For each release of data about a contracting process, add a row to `releases.csv` or the `releases` sheet. Each contracting process ought to have a unique `ocid`, and each release ought to have a unique release `id` within the scope of its contracting process. These identifiers are used to link up data across CSV files or Excel sheets.

In cases of one-to-many relationships – for example, one release can have many awards – data must be entered in a separate CSV file or Excel sheet. In those cases, you must enter the `ocid` of the contracting process, the `id` of the release, and other identifiers as appropriate among the first columns of the file or sheet.

Feel free to hide or remove unused columns.

## Converting to OCDS JSON

[See Flatten Tool's documentation](https://flatten-tool.readthedocs.io/en/latest/usage-ocds/#converting-a-populated-spreadsheet-to-json), or upload your spreadsheet to the [OCDS Data Review Tool](https://standard.open-contracting.org/review/).

## Maintenance

This assumes that the `standard` repository and this repository have the same parent directory on your system, and that the `standard` repository is checked out to the latest tag. Install Flatten Tool, change into this repository's directory, and run:

```shell
flatten-tool create-template --truncation-length 5 --schema=../standard/standard/schema/release-schema.json -o flat-template/template --root-id=ocid --main-sheet-name releases
```
