# Sample Data

[![Build Status](https://travis-ci.org/open-contracting/sample-data.svg?branch=master)](https://travis-ci.org/open-contracting/sample-data)

This repository holds sample data represented using the [Open Contracting Data Standard](http://ocds.open-contracting.org/standard/). It includes the following types of sample data:

* Fictional JSON and XLSX examples of releases and records, designed to demonstrate the key features of OCDS
* Blank templates, designed to provide a reference JSON file including all of the fields in the OCDS schema
* Flat templates, designed to provide a reference .csv and .xlsx files including all of the fields in OCDS
* Real examples, a collection of scraper scripts and samples of releases and records from real OCDS implementations

It should contain data aligned with the current version of the standard. Data aligned with previous versions of the standard may be found on named branches.

Pointers to externally available example data are found in the sources.md file.

## Test that sample data validates

```
pip install jsonschema
./validate.sh
```

## Licences

Each directory has its own README documenting the data source. Please note that the data in each folder is licensed under the license of the original publisher, which is documented in the README in each folder.
