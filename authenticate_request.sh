#!/bin/bash 
apiKey="7e71a1cf29aebcaed738be43eb126e12"
secret="d0050074ba"
curl -i \
-X GET \
-H 'Accept:application/json' \
-H 'Api-key:'$apiKey'' \
-H 'X-Signature:'$(echo -n ${apiKey}${secret}$(date +%s)|sha256sum|awk '{ print $1}')'' \
https://api.test.hotelbeds.com/hotel-api/1.0/status