# Moldova

OCDS output is available as a [bulk release download](http://opencontracting.date.gov.md/downloads).

(For reference, it is also available in the format `http://moldova-ocds.yipl.com.np/ocds/{CONTRACT-ID}/json` e.g. <http://moldova-ocds.yipl.com.np/ocds/89270/json>)

There were 12,639 available releases as of 2017/06/29.

Releases currently fail validation with the error:

    properties/parties/items/properties/additionalIdentifiers/type: {'scheme': 'eTenders', 'id': '', 'legalName': ''} is not of type 'array'

And many fail with errors like this:

    "properties/tender/properties/status/enum: 'Executarea contractului' is not one of ['planned', 'active', 'cancelled', 'unsuccessful', 'complete', None]
