Real world OCDS examples
========================

This folder contains real-world examples of OCDS data and scripts for fetching updated examples, and full data downloads.

Each completed folder contains:

* A ```fetch.py``` script which will get an updated set of examples. Run with, for example, `python australia/new-south-wales/fetch.py` (you will need the current directory in your Python path).
* A ```sample/releases``` folder which contains a small number of example releases, and a ```sample/records``` folder with a small number of example records.

The ```fetch.py``` scripts default to collecting around 10 publications. Use the command-line argument ```-a``` to fetch 'all' available publications and save them in an ```all``` folder (which git will ignore).

Once you have downloaded the publications, you can then transform to v1.1 of the OCDS schema if appropriate; validate them against the 1.1 schema, recording any errors; and finally, combine releases into records. This is done with:

* ```update_to_v1_1.py```: updates v1.0.2 OCDS releases to v1.1 of the schema, overwriting existing files. Run with `python update_to_v1_1.py -f path/to/releases`.
* ```validate.py```: validates releases against the v1.1 schema. This script adds a new top-level property called `validationErrors` to each release, storing details of any validation errors. Run with `python validate.py -f path/to/releases`.
* ```merge_releases.py```: merge releases into records. This script adds a new top-level property called `validationErrors` to each release, storing details of any validation errors. Run with `python merge_releases.py --filepath path/to/releases  --outfilepath path/to/records`.

You can then upload your validated, updated releases and records to the OCDS AWS bucket, in order to run queries against them. For example:

    aws s3 sync australia/new-south-wales/all/releases s3://ocds1/releases --exclude '.DS_Store' --exclude '.keep'
