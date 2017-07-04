Nigeria - Open Contracting Portal
=================================

OCDS output is available here: http://35.160.38.216/open_api and a release package containing all releases can be downloaded here: http://35.160.38.216/downloadSelected

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were 1,336 available releases as of 2017/06/29.

Currently all fail with e.g.

    Problem validating sample/releases/ocds-gyl66f-borbda-zt1ngs-ocds-gyl66f-borbda-zt1ngs.json
    properties/tender/properties/tenderers/items/properties/name/minLength: '' is too short
