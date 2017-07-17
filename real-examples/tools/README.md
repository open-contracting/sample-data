This directory contains tools for uploading releases and records to BigQuery, ready to for OCDS data users to run queries against them.

Upload files to BigQuery
------------------------

Before you upload files, you must remove fields not in the standard schema, and make some changes (e.g. all ID fields must become strings). You must also convert the releases to newline-delimited JSON. Use the conversion script to do this, for exmaple:

    python convert_releases_to_bigquery_schema.py -f ../mexico/grupo-aeroportuario/all/releases/

Now you can upload your releases to BigQuery. You will first need to install the [Cloud SDK tools](https://cloud.google.com/sdk/).

Note that this will *append* rows to existing tables - you therefore may want to delete the existing table before running this. You can delete tables in the BigQuery UI or via the command line.

To upload your newline-delimted JSON file of releases:

    bq load --source_format=NEWLINE_DELIMITED_JSON --schema=release-schema-bq.json --project_id ocds-172716 releases.mexico_grupo all-releases.json

Fix upload errors
-----------------

If you are uploading records this for a new publisher, you get BigQuery complaining about unknown columns, since it expects releases to conform exactly to the schema and does not like extra data.

You should delete these columns from the source data, using the conversion script.

If you see an error like:

    Only optional fields can be set to NULL. Field: tag; Value: NULL

It means that the field is missing: you need to insert it.

Running command-line queries
----------------------------

You can now query your table, for example:

bq  --project_id ocds-172716 query "SELECT COUNT(ocid) FROM releases.mexico_grupo"

Updating the schema
-------------------

There is a schema supplied here - `release-schema-bq.json`. If you need to update it, use:

    python convert_ocds_schema_to_bigquery.py

This expects a schema called `release-schema.json`, and outputs a BigQuery-formatted schema called `release-schema-bq.json`.
