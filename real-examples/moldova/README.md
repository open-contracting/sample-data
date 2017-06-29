Moldova
=======

OCDS output is available as a bulk release download from http://opencontracting.date.gov.md/downloads

(For reference, it is also available in the format http://moldova-ocds.yipl.com.np/ocds/{CONTRACT-ID}/json e.g. http://moldova-ocds.yipl.com.np/ocds/89270/json)

The process to obtain a sample:

    python3 fetch.py

Or to obtain all records:

    python3 fetch.py --all

There were 12,639 available records as of 2017/06/29.

This publisher only publishes releases, so you will need to transform the releases for v1.1, then merge the transformed releases into records (TODO). You can then validate both records and releases, and upload them to S3.

Note that currently every release fails validation with the errors:

    properties/parties/items/properties/additionalIdentifiers/type: {'scheme': 'eTenders', 'id': '', 'legalName': ''} is not of type 'array'

And many fail with errors like this:

    "properties/tender/properties/status/enum: 'Executarea contractului' is not one of ['planned', 'active', 'cancelled', 'unsuccessful', 'complete', None]
