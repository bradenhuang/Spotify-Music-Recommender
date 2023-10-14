import base64
import requests
import datetime
import json
import webbrowser
from secret import secrets
from urllib.parse import urlencode
from getcode.py import get_auth_code
from gettoken.py import get_token
from getliked.py import get_liked
from songfeatures.py import get_song_features


client_id = secrets['client_id']
client_secret = secrets['client_secret']


credentials = f"{client_id}:{client_secret}"
creds_b64 = base64.b64encode(credentials.encode())


def get_userid(token):
    url = "https://api.spotify.com/v1/me"
    header = {"Authorization" : "Bearer " + token}
    r = requests.get(url, headers=header)
    response = r.json()
    id = response['id']
    print(response)
    

def main():
    get_auth_code()
    code = str(input("Enter the code from the URL of the webpage: "))
    token = get_token(code)
    songs = get_liked(token)
    get_song_features(songs, token)

if __name__ == "__main__":
    main()


    