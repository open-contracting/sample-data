Mexico > Grupo Aeroportuario de la Ciudad de México
===================================================

OCDS files for major contracts of the Mexico City Airport project are accessible at https://datos.gob.mx/busca/organization/gacm

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were 271 available release packages as of 2017/07/03.

This publisher only publishes releases, so you will first need to transform the releases for v1.1 and validate them, then merge the transformed releases into records:

    python3 ../../update_to_v1_1.py -f sample/releases
    python3 ../../validate.py -f sample/releases

Currently they pass validation.

Then transform the releases into records:

    python ../../merge_releases.py -f sample/releases -o sample/records

Finally you can upload all records to S3:

    aws s3 sync sample/releases s3://ocds1/releases --exclude '.DS_Store' --exclude '.keep'
