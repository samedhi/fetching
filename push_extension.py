#! /usr/bin/env python

import json
import requests

# Site I got this information from:
# https://developer.chrome.com/webstore/using_webstore_api

# Url I get my oauth access token from (using extension.json)
# https://accounts.google.com/o/oauth2/auth?response_type=code&scope=https://www.googleapis.com/auth/chromewebstore&client_id=$CLIENT_ID&redirect_uri=urn:ietf:wg:oauth:2.0:oob
# =>
# https://accounts.google.com/o/oauth2/auth?response_type=code&scope=https://www.googleapis.com/auth/chromewebstore&client_id=39380323414-t66ulhnvda5aras6tulbf0mhcnftqua1.apps.googleusercontent.com&redirect_uri=urn:ietf:wg:oauth:2.0:oob

# CODE = # Get the CODE from the url above

# resp = requests.post('https://accounts.google.com/o/oauth2/token',
#                     data={'client_id': CLIENT_ID,
#                           'client_secret': CLIENT_SECRET,
#                           'code': CODE,
#                           'grant_type': 'authorization_code',
#                           'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'})
#
# Put it in 'refresh_token' in extension.json

with open('extension.json') as f:
    text = f.read()

JS = json.loads(text)

CLIENT_ID = JS['client_id']

CLIENT_SECRET = JS['client_secret']

REFRESH_TOKEN = JS['refresh_token']

resp = requests.post('https://accounts.google.com/o/oauth2/token',
                    data={'client_id': CLIENT_ID,
                          'client_secret': CLIENT_SECRET,
                          'refresh_token': REFRESH_TOKEN,
                          'grant_type': 'refresh_token',
                          'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'})

APP_ID = 'fmcklaikklmlfahjgdndacebapkpefan'

ACCESS_TOKEN = resp.json()['access_token']

filepath = 'target_extension.zip'
with open(filepath, 'rb') as fh:
    resp = requests.put('https://www.googleapis.com/upload/chromewebstore/v1.1/items/%s' % APP_ID,
                        data=fh.read(),
                        headers={'Authorization': "Bearer %s" % ACCESS_TOKEN,
                                 'x-goog-api-version': "2"},
                        params={'file': filepath})

print resp.text

if resp.status_code != 200:
    print resp.text
