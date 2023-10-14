import requests

def get_song_features(songs, token, batch_size=100):
    header = {"Authorization" : "Bearer " + token}
    url = "https://api.spotify.com/v1/audio-features?"

    for i in range(0, len(songs), batch_size):
        batch = songs[i:i+batch_size]  
        
        ids = ','.join(song['id'] for song in batch)

        track_url = f"{url}ids={ids}"
        r = requests.get(track_url, headers=header)
        features_batch = r.json()

        for song, features in zip(batch, features_batch['audio_features']):
            song["Audio Features"] = features
    