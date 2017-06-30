Canada > City of Montreal
=========================

The City of Montreal provide awards information in OCDS format at https://ville.montreal.qc.ca/vuesurlescontrats/

The data is accessible in OCDS format from the 'Export' button, or via the API e.g. https://ville.montreal.qc.ca/vuesurlescontrats/api/releases.json?limit=10000&offset=0

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were 90,517 releases as of 2016/06/29.

This publisher only publishes releases, so you will first need to transform the releases for v1.1 and validate them, then merge the transformed releases into records:

    python3 ../../update_to_v1_1.py -f sample/releases
    python3 ../../validate.py -f sample/releases

Currently they all fail with:

    properties/tag/type: 'award' is not of type 'array'

Then transform the releases into records:

    python ../../merge_releases.py -f sample/releases -o sample/records

Finally you can upload all to S3:

    aws s3 sync sample/releases s3://ocds1/releases --exclude '.DS_Store' --exclude '.keep'
