Canada > City of Montreal
=========================

The City of Montreal provide awards information in OCDS format at https://ville.montreal.qc.ca/vuesurlescontrats/

The data is accessible in OCDS format from the 'Export' button, or via the API e.g. https://ville.montreal.qc.ca/vuesurlescontrats/api/releases.json?limit=10000&offset=0

Note that there seem to be some duplicate release IDs: e.g. `f3c0841b7de8ff3e335518790948349e38091257` occurs more than once.

There were 85,533 unique release IDs as of 2016/06/29.

Currently the releases all fail validation with:

    properties/tag/type: 'award' is not of type 'array'
