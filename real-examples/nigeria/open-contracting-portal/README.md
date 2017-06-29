Nigeria - Open Contracting Portal
=================================

OCDS output is available here: http://35.160.38.216/open_api and a release package containing all releases can be downloaded here: http://35.160.38.216/downloadSelected

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were 1,336 available releases as of 2017/06/29.

This publisher only publishes releases, so you will first need to transform the releases for v1.1 and validate them, then merge the transformed releases into records:

    python3 ../../update_to_v1_1.py -f sample/releases
    python3 ../../validate.py -f sample/releases

Currently all fail with e.g.

    Problem validating sample/releases/ocds-gyl66f-borbda-zt1ngs-ocds-gyl66f-borbda-zt1ngs.json
    properties/tender/properties/tenderers/items/properties/name/minLength: '' is too short

Then transform the releases into records:

    python ../../merge_releases.py -f sample/releases -o sample/records

Finally you can upload all records to S3:

    aws s3 sync sample/releases s3://ocds1/releases --exclude '.DS_Store' --exclude '.keep'
