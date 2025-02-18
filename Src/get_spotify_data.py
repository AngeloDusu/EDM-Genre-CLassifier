import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get client ID and Secret from .env
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Auth using client credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

def get_tracks_by_genre_year(genre, start_year=2020, total=1000):
    """
    Ambil semua lagu dari genre tertentu dengan filter tahun rilis.
    """
    track_list = []
    offset = 0

    while len(track_list) < total:
        results = sp.search(q=f'genre:{genre}, year:{start_year}-2025', type='track', limit=50, offset=offset)
        tracks = results['tracks']['items']
        if not tracks:
            break

        for track in tracks:
            track_info = {
                'track_name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'release_date': track['album']['release_date'],
                'spotify_url': track['external_urls']['spotify'],
                'track_id': track['id'],
                'popularity': track['popularity']  # Ambil juga popularitas lagu
            }
            track_list.append(track_info)
        
        offset += 50  # Geser ke halaman berikutnya

    return track_list

def get_audio_features(track_ids, batch_size=50):
    """
    Ambil fitur audio dari daftar track_id menggunakan Spotify API.
    """
    audio_features = []
    for i in range(0, len(track_ids), batch_size):
        batch = track_ids[i:i+batch_size]
        features = sp.audio_features(batch)
        audio_features.extend(features)
        time.sleep(1)  # Hindari rate limit
    
    return audio_features

# Ambil data untuk dua genre: EDM & Dance/Electronic
genres = ["edm", "dance/electronic"]
all_tracks = []

for genre in genres:
    print(f"Fetching songs for genre: {genre}")
    genre_tracks = get_tracks_by_genre_year(genre, start_year=2020, total=900)
    all_tracks.extend(genre_tracks)

# Convert to DataFrame
df = pd.DataFrame(all_tracks)

# Ambil fitur audio berdasarkan track_id
track_ids = df["track_id"].tolist()
audio_features = get_audio_features(track_ids)

# Convert fitur audio ke DataFrame
df_audio = pd.DataFrame(audio_features)

# Gabungkan data lagu dengan fitur audio berdasarkan track_id
df_final = df.merge(df_audio, on="track_id", how="left")

# Pastikan folder Dataset ada
output_path = "D:\.vscode\kodingan\EDM-Genre-Classifier\Dataset\edm_2.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Simpan ke CSV
df_final.to_csv(output_path, index=False, encoding='utf-8')

print("✅ Dataset EDM & Dance/Electronic dengan fitur audio berhasil disimpan!")
