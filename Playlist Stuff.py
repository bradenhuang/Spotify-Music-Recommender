def get_playlists(token):
    playlists = []
    url = "https://api.spotify.com/v1/me/playlists"
    header = auth_header(token)
    r = requests.get(url, headers=header)
    json_playlists = r.json()
    items = json_playlists.get('items', [])
    
    for playlist in items:
        if playlist is not None:
            playlists.append({
                "name": playlist['name'],
                'id': playlist['id'],
                'uri': playlist['tracks']['href']
            })
    
    return playlists
    
def get_playlist_songs(playlists, token):
    for pl in playlists:
        playlist_tracks = []  
        url = f"{pl['uri']}?limit=50"
        header = auth_header(token)
        
        
        r = requests.get(url, headers=header)
        results = r.json()
        extract = results['items']
        
        for i in extract:
            if i is not None:
                track = i['track']
                artist_name = track['artists'][0]['name'] if track['artists'] else 'Unknown Artist'
                playlist_tracks.append({  
                    'Song_Name': track['name'],
                    'Album' : track['album']['name'],
                    "Artist" : artist_name,
                    "Cover" : track['album']['images'][0]['url'] if 'images' in track['album'] and track['album']['images'] else 'No Image',
                    'Link' : track['external_urls']['spotify'],
                    'id' : track['id'],
                    'Preview Link' : track['preview_url']
                })

        pl['tracks'] = playlist_tracks

        if results.get('next', None) is not None:
            url = results['next']
        elif results.get('tracks', None) is not None:
            url = results['tracks']['next']
        else:
            break

    return playlists