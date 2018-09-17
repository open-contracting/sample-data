# Real world OCDS examples

This folder contains real-world examples of OCDS data.

Each publisher directory contains:

* A ```sample/releases``` folder which contains a small number of example releases, and a ```sample/records``` folder with a small number of example records.

## Transform data

Once you have downloaded the releases, you can then transform to v1.1 of the OCDS schema, if they are published under a previous schema. Do this with:

    python update_to_v1_1.py -f path/to/releases

Note that this will overwrite the existing files.

## Merge records to releases

Finally you may also wish to combine releases into records. This is done with:

    python merge_releases.py --filepath path/to/releases  --outfilepath path/to/records

## Upload data to BigQuery

You can then upload the transformed records and releases to BigQuery, which lets you run rapid queries using SQL in the cloud. This process is described in `tools/README.md`.
