# Ukraine - ProZorro

[Live data](https://public.api.openprocurement.org/api/2.3/tenders), in a format based on OCDS, is available from ProZorro [via the Open Procurement API](http://api-docs.openprocurement.org/en/latest/).

Individual releases can be fetched by appending their ID onto `https://public.api.openprocurement.org/api/2.3/tenders/` such as <https://public.api.openprocurement.org/api/2.3/tenders/09076ffc415e4d57ad7046aacc91b6e1>

[Bulk releases](http://ocds.prozorro.openprocurement.io/) of ProZorro data are available in formats with and without OCDS extensions.

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were around 930,000 available releases as of 2017/06/29.

Currently they all fail with:

    properties/tag/items/enum: 'bid' is not one of ['planning', 'tender', 'tenderAmendment', 'tenderUpdate', 'tenderCancellation', 'award', 'awardUpdate', 'awardCancellation', 'contract', 'contractUpdate', 'contractAmendment', 'implementation', 'implementationUpdate', 'contractTermination', 'compiled']
