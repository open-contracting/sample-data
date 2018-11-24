# Blank template

This folder contains, for each version of OCDS, a blank file that corresponds to the release schema.

## Maintenance

This template is generated using a [fork of json-schema-random](https://github.com/open-contracting/json-schema-random).

Change into a directory containing the `standard` and `sample-data` repositories. Then, clone this repository and install its dependencies:

```shell
git clone https://github.com/open-contracting/json-schema-random.git
cd json-schema-random
npm install .
```

To regenerate all files, run (in bash shell):

```shell
for tag in `git -C ../standard tag | grep '1__\d__\d'`; do
  git -C ../standard checkout $tag;
  node cli.js ../standard/standard/schema/release-schema.json --no-random --no-additional > ../sample-data/blank-template/release-template-$tag.json;
done
git -C ../standard checkout 1.1-dev
```

To regenerate one file, set a `tag` environment variable and run:

```shell
git -C ../standard checkout $tag;
node cli.js ../standard/standard/schema/release-schema.json --no-random --no-additional > ../sample-data/blank-template/release-template-$tag.json
git -C ../standard checkout 1.1-dev
```

Remove deprecated fields by opening the `blank-template` directory in a text editor and using this regular expression to search deprecated fields and replace with empty strings:

```text
[,\n ]*"[a-zA-Z]+": "deprecated"
```

Change into this repository's directory, and indent the files with two spaces:

```shell
pip install ocdskit
ocsdkit indent -r blank-template
```
