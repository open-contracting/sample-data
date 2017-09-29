# Blank template

This folder contains a blank JSON file according to the Open Contracting Data Standard JSON release schemas.

## Generation

This template was generated using the [Open Contracting fork of JSON-schema-random](https://github.com/open-contracting/json-schema-random).

You will need to clone the repository, switch to the opencontracting branch, and install node dependencies:

```
git clone https://github.com/open-contracting/json-schema-random.git
git checkout opencontracting
npm install .
```

And then run the command:

```
node cli.js ../standard/standard/schema/release-schema.json --no-random --no-additional > ../sample-data/blank-template/release-template-1__0__0.json
```

replacing schema versions and output names appropriate.

To remove deprecated fields, run a regex search and replace against the following string:

```
[,\n ]*"[a-zA-Z]+": "deprecated"[,\n]*
```

and then format the JSON before saving.
