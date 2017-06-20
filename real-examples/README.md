Real world OCDS examples
========================

This folder contains real-world examples of OCDS data and scripts for fetching updated selections.

Each folder may contain:

* A ```fetch.py``` script which will get an updated set of examples
* A ```sample``` folder which contains a small number of example releases, and (if appropriate) a ```sample/records``` folder with a small number of example records.

The ```fetch.py``` script should default to collecting 100 or fewer releases (unless it is downloading a bulk file with a higher number in). It should accept a command line argument ```-a``` to fetch 'all' available releases and save them in an ```all``` folder. Where the default publication is records, the script should also offer a ```-r``` argument to download releases as well as records.

There are two utilities in this folder:

* ```update.py```: updates v1.0.2 OCDS releases to v1.1 of the schema.
* ```validate.py```: validates releases against the v1.1 schema. This script adds a new top-level property called `validationErrors` to each release, storing details of any validation errors.

## Current status

Most folders contain stub entries with README files, but no example data or scripts.

The folders with real data in are currently:

* uk-contracts-finder
* paraguay
