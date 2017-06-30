Taiwan
======

Sample data from 2014 is available at http://data.dsp.im/dataset/taiwan-open-contracting

Direct download link to larger dataset: http://data.dsp.im/dataset/963c0c3d-49ac-4a66-b8fa-f56c8166bb91/resource/0abbe767-c940-49fe-80d3-bd68268f508e/download/2014-02.json

Read more at http://www.open-contracting.org/2016/03/02/open-contracting-in-taiwan-the-journey-so-far/

Note that these releases lack an `id` property.

The process to obtain a sample:

    python3 fetch.py

Or to obtain all releases:

    python3 fetch.py --all

There were 707 releases as of 2016/06/29.

This publisher only publishes releases, so you will first need to transform the releases for v1.1 and validate them, then merge the transformed releases into records:

    python3 ../update_to_v1_1.py -f sample/releases
    python3 ../validate.py -f sample/releases

Currently they all fail with:

    properties/tag/type: 'awardNotice' is not of type 'array'

Then transform the releases into records:

    python ../merge_releases.py -f sample/releases -o sample/records

Finally you can upload all to S3:

    aws s3 sync sample/releases s3://ocds1/releases --exclude '.DS_Store' --exclude '.keep'
