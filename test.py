"""
I don't know how it works for other campus, so maybe the api url is different,
if so you would have to change the token_url with the corresponding one, if it works using OAuth2.
If it's not OAuth2 and just a basic restful api you might need to redo the whole boto.py and other
"""

import os
import sys
import json

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

UID_42 = os.getenv('UID_42')
SECRET_42 = os.getenv('SECRET_42')
token_url = "https://api.intra.42.fr/oauth/token"

print(f'uid: {UID_42}')
print(f'secret: {SECRET_42}')
# Header with client_id and client_secret easier to send key and fetch token
auth = HTTPBasicAuth(UID_42, SECRET_42)

# start client
_client = BackendApplicationClient(client_id=UID_42);
# start session
api42 = OAuth2Session(client=_client)


try:
    token = api42.fetch_token(token_url=token_url, auth=auth)
except:
    print("Problem with your token you probably didn't export properly your key")
    raise
    sys.exit(1)

try:
    r = api42.get('https://api.intra.42.fr/v2/campus?page[size]=100')
except:
    print("Didn't receive response from endpoint")
    sys.exit(1)
else:
    i = 0
    res = r.json()
    for campus in res:
        # [index]: campus_id campus_name / campus_website
        print(f"[{i}]: {campus['id']} {campus['name']} / {campus['website']}")
        i += 1

# if you want to test if you have the proper put flag = 1
flag = 0
if (flag == 1):
    try:
        # modify your_campus_id with the id number of your campus and put your login at the end
        r = api42.get('https://api.intra.42.fr/v2/campus/your_campus_id/users?filter[login]=your_login')
    except:
        print("Didn't receive a response")
        raise
        sys.exit(1)
    res = r.json()
    print("\n")
    # you should get a result with all of your info
    print(res)
sys.exit(0)
