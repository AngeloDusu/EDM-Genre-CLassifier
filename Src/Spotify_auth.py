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
