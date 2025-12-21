import time
import random
import requests
from config import CLIENT_ID, CLIENT_SECRET, MAX_RETRIES
import ast 
import math


# authentication
def get_access_token():
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

access_token = get_access_token()
headers = {"Authorization": f"Bearer {access_token}"}
print("Access token OK.\n")

def get_json(url, params=None, max_retries=MAX_RETRIES):
    global access_token, headers
    for attempt in range(max_retries):
        resp = requests.get(url, headers=headers, params=params)

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", "3"))
            wait = retry_after + random.uniform(0.5, 2.0)
            print(f"429 Too Many Requests. Sleeping {wait:.1f}s...")
            time.sleep(wait)
            continue

        if resp.status_code == 401:
            print("401 Unauthorized. Refreshing token...")
            access_token = get_access_token()
            headers = {"Authorization": f"Bearer {access_token}"}
            time.sleep(1.0)
            continue

        if resp.status_code >= 400:
            print(f"Error {resp.status_code} for URL: {url}")
            return None

        try:
            return resp.json()
        except Exception as e:
            print("JSON decode error:", e)

        backoff = (1.5 ** attempt) + random.uniform(0, 1)
        time.sleep(backoff)

    print(f"Failed after {max_retries} retries: {url}")
    return None

# Function to map Genres
def map_playlist_genres(genre_list_raw, mapping_df):
    mapping_df["Subgenre_norm"] = mapping_df["Subgenre"].str.strip().str.lower()
    mapping_df["Primary_norm"] = mapping_df["Primary Genre"].str.strip()
    sub_to_parent = dict(zip(mapping_df["Subgenre_norm"], mapping_df["Primary_norm"]))

    if isinstance(genre_list_raw, str):
        try:
            genre_list = ast.literal_eval(genre_list_raw)
        except Exception:
            genre_list = [genre_list_raw]
    elif isinstance(genre_list_raw, list):
        genre_list = genre_list_raw
    else:
        return [], []  

    mapped = []
    unmapped = []

    for g in genre_list:
        if not isinstance(g, str):
            unmapped.append(g)
            continue

        g_norm = g.strip().lower()

        if g_norm in sub_to_parent:
            mapped.append(sub_to_parent[g_norm])
        else:
            unmapped.append(g)

    mapped = sorted(set(mapped))
    unmapped = sorted(set(unmapped))

    return mapped, unmapped

def genre_breadth_score(n):
    if n <= 1:
        return 100
    if n >= 50:
        return 0
    return round(100 * (1 - math.log(n) / math.log(50)), 1)


def genre_density_score(total_tracks, primary_genre_diversity):
    n = max(primary_genre_diversity, 1)
    density = total_tracks / n

    if density >= 80:
        return 100
    if density <= 5:
        return 0

    return round(100 * (density - 5) / (80 - 5), 1)


def artist_focus_score(total_tracks, unique_artists):
    if total_tracks == 0:
        return 0

    ratio = unique_artists / total_tracks

    if ratio <= 0.3:
        return 100
    if ratio >= 1.0:
        return 0

    return round(100 * (1 - (ratio - 0.3) / (1.0 - 0.3)), 1)


def musinique_focus_score(row):
    s1 = genre_breadth_score(row["primary_genre_diversity"])
    s2 = genre_density_score(row["total_tracks"], row["primary_genre_diversity"])
    s3 = artist_focus_score(row["total_tracks"], row["unique_artists"])

    return round(
        0.45 * s1 +   # genre entropy proxy
        0.30 * s2 +   # density
        0.25 * s3,   # artist coherence
        1
    )
