import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
import time 
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# gte clint ID and Secret from .env
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# auth using client credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))


def get_tracks_by_genre(genre, total_limit=500, batch_size=50, start_year = 2021, end_year = 2025):
    """
    Ambil daftar lagu berdasarkan genre dengan pagination.
    total_limit = jumlah total lagu yang diinginkan
    batch_size = jumlah lagu per request (maks 50)
    """

    track_list = []
    for offset in range(0, total_limit, batch_size):
        results = sp.search(q=f'genre:{genre} year:{start_year}-{end_year}', type='track', limit=batch_size, offset=offset)
        tracks = results['tracks']['items']

        for track in tracks:
            track_info = {
                'track_name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'release_date': track['album']['release_date'],
                'spotify_url': track['external_urls']['spotify'],
                'track_id': track['id']
            }
            track_list.append(track_info)

        # Tambahkan delay agar tidak kena rate limit
        time.sleep(1)  

    return track_list

if __name__ == "__main__" :
    genre = "edm"
    limit = 500

    print(f"Taking {limit} song from {genre}")
    edm_tracks = get_tracks_by_genre(genre, limit)


    # Simpan ke DataFrame
    df = pd.DataFrame(edm_tracks)
    df.to_csv("D:\.vscode\kodingan\EDM-Genre-Classifier\Dataset\edm_tracks.csv", index=False)
    print("Dataset EDM berhasil disimpan!")
  

