## New South Wales

The NSW eTendering API is documented at https://github.com/NSW-eTendering/NSW-eTendering-API

I believe that if we retrieve releases from these three categories, following the `next` links, we will have full coverage (but we should check this):

    https://tenders.nsw.gov.au/?event=public.api.planning.search&ResultsPerPage=1000
    https://tenders.nsw.gov.au/?event=public.api.tender.search&ResultsPerPage=1000
    https://tenders.nsw.gov.au/?event=public.api.contract.search&ResultsPerPage=1000

As of 2017/07/04 there are around 20,000 releases.
