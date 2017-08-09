## Ukraine - ProZorro

Live data, in a format based on  OCDS is available from ProZorro [via the Open Procurement API](http://api-docs.openprocurement.org/en/latest/) and available at https://public.api.openprocurement.org/api/2.3/tenders

Individual releases can be fetched by appending their ID onto https://public.api.openprocurement.org/api/2.3/tenders/ such as https://public.api.openprocurement.org/api/2.3/tenders/09076ffc415e4d57ad7046aacc91b6e1

Bulk releases of ProZorro data are available at http://ocds.prozorro.openprocurement.io/ in formats with and without OCDS extensions.

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were around 1 million available releases as of 2017/06/29.

This publisher only publishes releases, so you will first need to transform the releases for v1.1 and validate them, then merge the transformed releases into records:

    python3 ../update_to_v1_1.py -f sample/releases
    python3 ../validate.py -f sample/releases

Currently they all fail with:

    properties/tag/items/enum: 'bid' is not one of ['planning', 'tender', 'tenderAmendment', 'tenderUpdate', 'tenderCancellation', 'award', 'awardUpdate', 'awardCancellation', 'contract', 'contractUpdate', 'contractAmendment', 'implementation', 'implementationUpdate', 'contractTermination', 'compiled']

Then transform the releases into records:

    python ../merge_releases.py -f sample/releases -o sample/records

Finally you can upload all records to S3:

    aws s3 sync sample/releases s3://ocds1/releases --exclude '.DS_Store' --exclude '.keep'