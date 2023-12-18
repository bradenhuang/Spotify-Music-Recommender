import requests
    
def get_playlists(token, playlists):
    url = "https://api.spotify.com/v1/me/playlists"
    header = {"Authorization" : "Bearer " + token}
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

def playlist_select(playlists):
    if len(playlists) > 0:
        for index, playlist in enumerate(playlists, start=1):
            print(f"{index}. {playlist['name']}")
        print(f"{len(playlists)+1}. Import all")
        choice = input("Please enter the number of the playlist you wish to select: ")
        return choice 
             
def get_playlist_songs(playlists, token, songs):
    url = f"{playlists['uri']}?limit=50"
    header = {"Authorization" : "Bearer " + token}
    
    while True:
        r = requests.get(url, headers=header)
        results = r.json()
        extract = results['items']  

        for i in extract:
            if i:
                track = i.get('track')
                if track:
                    artist_name = track['artists'][0]['name'] if track.get('artists') else 'Unknown Artist'
                    external_urls = track.get('external_urls', {})
                    spotify_link = external_urls.get('spotify', 'No Link')
                    if spotify_link == "No Link":
                        continue
                    songs.append({
                        'Song_Name': track['name'],
                        'Album': track['album']['name'],
                        "Artist": artist_name,
                        "Cover": track['album']['images'][0]['url'] if 'images' in track['album'] and track['album']['images'] else 'No Image',
                        'Link' : spotify_link,
                        'id': track['id'],
                        'Preview Link': track['preview_url']
                    }) 
        if (results.get('next',None) is not None):
            url = results['next']
        elif (results.get('tracks',None) is not None):
            url = results['tracks']['next']
        else:
            break
    print (len(songs))
    return songs