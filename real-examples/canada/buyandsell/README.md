Canada > BuyAndSell.gc.ca
==============================

Public Works and Government Services Canada (PWGSC) ran an early Open Contracting Data Standard (OCDS) Pilot generating bulk exports of data, which are available at https://buyandsell.gc.ca/procurement-data/open-contracting-data-standard-pilot

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were 36,164 available releases as of 2017/06/29.

This publisher only publishes releases, so you will first need to transform the releases for v1.1 and validate them, then merge the transformed releases into records:

    python3 ../../update_to_v1_1.py -f sample/releases
    python3 ../../validate.py -f sample/releases

Currently they all fail with:

    Problem validating sample/releases/ocds-34a6hz-01B68-160000_001_CY-01B68-160000_001_CY.json
    properties/buyer/properties/name/minLength: '' is too short

Then transform the releases into records:

    python ../../merge_releases.py -f sample/releases -o sample/records

Finally you can upload all records to S3:

    aws s3 sync sample/releases s3://ocds1/releases --exclude '.DS_Store' --exclude '.keep'
