import base64
import requests
import datetime
import json
import webbrowser
from secret import secrets
from urllib.parse import urlencode

client_id = secrets['client_id']
client_secret = secrets['client_secret']

def get_auth_code():

    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-library-read playlist-read-private"
        }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))