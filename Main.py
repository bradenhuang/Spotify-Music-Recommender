import base64
import requests
import datetime
import json
import webbrowser
from secret import secrets
from urllib.parse import urlencode
from getcode import get_auth_code
from gettoken import get_token
from getliked import get_liked
from songfeatures import get_song_features
from playlistoperations import *


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
    songs = []
    playlists = []
    get_auth_code()
    code = str(input("Enter the code from the URL of the webpage: "))
    token = get_token(code)
    #songs = get_liked(token,songs)
    #get_song_features(songs, token)
    #playlists = get_playlists(token, playlists)
    #pchoice = playlist_select(playlists)
    #get_playlist_songs_all(playlists,token,songs)

    
    """with open("output.txt", "w") as file:
        for song in songs:
            song_json = json.dumps(song, ensure_ascii=False)  # Convert the dictionary to a JSON string
            file.write(song_json + "\n")  # Write the JSON string to the file
        print('all songs added to file')"""


if __name__ == "__main__":
    main()


    