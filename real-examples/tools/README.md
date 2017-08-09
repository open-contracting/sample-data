This directory contains tools for uploading releases and records to BigQuery, ready to for OCDS data users to run queries against them.

Convert files to BigQuery schema
--------------------------------

Before you upload files, you must remove fields not in the standard schema, and make some changes (e.g. all ID fields must become strings). You must also convert the releases to newline-delimited JSON.

The conversion script supplied will do this for you. To run it:

    python convert_releases_to_bigquery_schema.py -f ../mexico/grupo-aeroportuario/all/releases/

This creates a new newline-delimited JSON file called `all-releases.json`, and does not change your original files.

Upload files to BigQuery
------------------------

Now you can upload your releases to BigQuery. First install the [Cloud SDK tools](https://cloud.google.com/sdk/). Then, to upload your newline-delimted JSON file of releases:

    bq load --source_format=NEWLINE_DELIMITED_JSON --schema=release-schema-bq.json --project_id ocds-172716 releases.mexico_grupo all-releases.json

Change `releases.mexico_grupo` to the name of the table you want to create.

If the table already exists, this will *append* rows - you therefore probably want to delete any existing table before running this. You can delete tables in the BigQuery UI or via the command line.

If you are uploading records this for a new publisher, you may get BigQuery complaining about unknown columns, since it expects releases to conform exactly to the schema and does not like extra data. You should use the conversion script above to delete these columns from the source data.

If you see an error like:

    Only optional fields can be set to NULL. Field: tag; Value: NULL

It means that the field is missing and you need to insert it.

Querying BigQuery files
-----------------------

You can now query your table from the command line, for example:

bq  --project_id ocds-172716 query "SELECT COUNT(ocid) FROM releases.mexico_grupo"

You can also use the BigQuery UI to run queries.

Updating the schema
-------------------

There is a schema supplied here - `release-schema-bq.json`. If you need to update it, use:

    python convert_ocds_schema_to_bigquery.py

This expects a schema called `release-schema.json`, and outputs a BigQuery-formatted schema called `release-schema-bq.json`.
