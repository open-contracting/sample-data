Canada > City of Montreal
=========================

The City of Montreal provide awards information in OCDS format at https://ville.montreal.qc.ca/vuesurlescontrats/

The data is accessible in OCDS format from the 'Export' button, or via the API e.g. https://ville.montreal.qc.ca/vuesurlescontrats/api/releases.json?limit=10000&offset=0

Note that there seem to be some duplicate release IDs: e.g. `f3c0841b7de8ff3e335518790948349e38091257` occurs more than once.

There were 89601 release files as of 2017/08/07.

Currently the releases all fail validation with:

    properties/tag/type: 'award' is not of type 'array'
