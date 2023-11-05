#!/bin/bash 
client_id = 'eLWoFfHf0ngMXRZoClATedEWUIRAsFDB'
client_secret = '0oEEu6nk1da8MqeF'
curl "https://test.api.amadeus.com/v1/security/oauth2/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
