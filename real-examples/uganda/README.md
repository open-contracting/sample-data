Uganda
======

The Government of Uganda Procurement Portal provides an API onto data in OCDS format.

The endpoint is linked from <http://gpp.ppda.go.ug/open-data/> and data is provided at <http://gpp.ppda.go.ug/api/v1/releases>

The API can be filtered for each kind of release:

* Planning: <http://gpp.ppda.go.ug/api/v1/releases?tag=planning>

* Tender: <http://gpp.ppda.go.ug/api/v1/releases?tag=tender>

* Award: <http://gpp.ppda.go.ug/api/v1/releases?tag=award>

* Contract: <http://gpp.ppda.go.ug/api/v1/releases?tag=contract>

At present (October 2017), we are not certain how releases are being handled, and release IDs do not appear to be changed across releases, so the script fetches separate directories of planning, tender, award and contracts.

Single records can be accessed via ocid, such as: <http://gpp.ppda.go.ug/api/v1/releases/ocds-rdvc92-1508158255>
