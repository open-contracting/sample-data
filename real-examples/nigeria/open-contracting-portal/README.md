# Nigeria - Open Contracting Portal

OCDS output is [available](http://nigeriaoc.org/open_api) and a release package containing all releases can be [downloaded](http://nigeriaoc.org/downloadSelected).

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were 1,336 available releases as of 2017/08/07.

Currently most fail validation with e.g.

    Problem validating sample/releases/ocds-gyl66f-borbda-zt1ngs-ocds-gyl66f-borbda-zt1ngs.json
    properties/tender/properties/tenderers/items/properties/name/minLength: '' is too short
