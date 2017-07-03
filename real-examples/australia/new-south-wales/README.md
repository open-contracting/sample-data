## New South Wales

The NSW eTendering API is documented at https://github.com/NSW-eTendering/NSW-eTendering-API

I believe that if we retrieve releases from these three categories, following the `next` links, we will have full coverage (but we should check this):

    https://tenders.nsw.gov.au/?event=public.api.planning.search&ResultsPerPage=1000
    https://tenders.nsw.gov.au/?event=public.api.tender.search&ResultsPerPage=1000
    https://tenders.nsw.gov.au/?event=public.api.contract.search&ResultsPerPage=1000

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were around 1 million available releases as of 2017/06/29.

This publisher only publishes releases, so you will first need to transform the releases for v1.1 and validate them, then merge the transformed releases into records:

    python3 ../../update_to_v1_1.py -f sample/releases
    python3 ../../validate.py -f sample/releases

Currently they pass validation.

Then transform the releases into records:

    python ../../merge_releases.py -f sample/releases -o sample/records

Finally you can upload all records to S3:

    aws s3 sync sample/releases s3://ocds1/releases --exclude '.DS_Store' --exclude '.keep'
