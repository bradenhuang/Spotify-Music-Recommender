import base64
import requests
import datetime
import json
import webbrowser
from secret import secrets
from urllib.parse import urlencode
from getcode import get_auth_code


client_id = secrets['client_id']
client_secret = secrets['client_secret']


credentials = f"{client_id}:{client_secret}"
creds_b64 = base64.b64encode(credentials.encode())

def get_token(code):

    url = "https://accounts.spotify.com/api/token"
    
    token_data = {
        "grant_type" : "authorization_code",
        "code" : code,
        "redirect_uri": "http://localhost:7777/callback"
    }

    token_headers = {
        "Authorization": f"Basic {creds_b64.decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post(url, data=token_data, headers=token_headers)
    valid = r.status_code in range (200,299)

    if valid:
        token_response = r.json()
        now = datetime.datetime.now()
        token = token_response['access_token']
        expires = token_response['expires_in']
        expiry = now + datetime.timedelta(seconds=expires)
        expired = expiry < now
        return token  