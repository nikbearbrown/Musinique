"""
Configuration and authentication for Spotify API.
"""

import os
import base64
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080/")

SCOPE = "playlist-read-private"

# Keywords for playlist search
KEYWORDS = [
    "indie",
    "indie pop",
    "indie rock",
    "indie folk",
    "bedroom pop",
    "lofi",
    "unsigned artist",
    "emerging artist",
]

# API rate limiting
REQUEST_DELAY = 0.15  # seconds between requests
MAX_PLAYLISTS_PER_KEYWORD = 1000


def get_spotify_client():
    """
    Get authenticated Spotify client using OAuth.
    
    Returns:
        spotipy.Spotify: Authenticated Spotify client
    """
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        open_browser=True
    ))


def get_client_credentials_token():
    """
    Get access token using client credentials flow.
    
    Returns:
        str: Access token
    """
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        headers={"Authorization": f"Basic {auth}"}
    )
    
    return r.json()["access_token"]


def get_auth_headers():
    """
    Get authorization headers for API requests.
    
    Returns:
        dict: Headers with Bearer token
    """
    token = get_client_credentials_token()
    return {"Authorization": f"Bearer {token}"}
