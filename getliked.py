import requests

def get_liked(token):
    songs = []
    url = "https://api.spotify.com/v1/me/tracks?limit=50"
    headers = {"Authorization" : "Bearer " + token}
    
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