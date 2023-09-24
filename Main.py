import base64
import requests
import datetime
import json
import webbrowser
from secret import secrets
from urllib.parse import urlencode

client_id = secrets['client_id']
client_secret = secrets['client_secret']


credentials = f"{client_id}:{client_secret}"
creds_b64 = base64.b64encode(credentials.encode())

def get_auth_code():

    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-library-read playlist-read-private"
        }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
    
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

def auth_header(token):
    return {"Authorization" : "Bearer " + token}


def get_userid(token):
    url = "https://api.spotify.com/v1/me"
    header = auth_header(token)
    r = requests.get(url, headers=header)
    response = r.json()
    id = response['id']
    print(response)

def get_liked(token):
    songs = []
    url = "https://api.spotify.com/v1/me/tracks?limit=50"
    headers = auth_header(token)
    
    while True:
        r = requests.get(url, headers=headers)
        results = r.json()
        extract = results['items']  

        for i in extract:
            if (i is not None):
                track = i['track']
                artist_name = track['artists'][0]['name'] if track['artists'] else 'Unknown Artist'
                songs.append({
                    'Song_Name': track['name'],
                    'Album' : track['album']['name'],
                    "Artist" : artist_name,
                    "Cover" : track['album']['images'][0]['url'] if 'images' in track['album'] and track['album']['images'] else 'No Image',
                    'Link' : track['external_urls']['spotify'],
                    'id' : track['id'],
                    'Preview Link' : track['preview_url']
                })
            
        if (results.get('next',None) is not None):
            url = results['next']
        elif (results.get('tracks',None) is not None):
            url = results['tracks']['next']
        else:
            break
    return songs

def get_song_features(songs, token, batch_size=100):
    header = auth_header(token)
    url = "https://api.spotify.com/v1/audio-features?"

    for i in range(0, len(songs), batch_size):
        batch = songs[i:i+batch_size]  
        
        ids = ','.join(song['id'] for song in batch)

        track_url = f"{url}ids={ids}"
        r = requests.get(track_url, headers=header)
        features_batch = r.json()

        for song, features in zip(batch, features_batch['audio_features']):
            song["Audio Features"] = features
    


def main():
    get_auth_code()
    code = str(input("Enter the code from the URL of the webpage: "))
    token = get_token(code)
    songs = get_liked(token)
    get_song_features(songs, token)

if __name__ == "__main__":
    main()


    