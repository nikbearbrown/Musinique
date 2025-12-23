import time
import pandas as pd
from collections import Counter
from utils import get_json, get_access_token

# Fetch all playlists for this curator
def fetch_curator_playlists(user_id, TARGET_CURATOR_NAME):    
    playlists = []
    offset = 0
    limit = 50

    print(f"Fetching playlists for curator: {TARGET_CURATOR_NAME} ({user_id})")

    while True:
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        params = {"limit": limit, "offset": offset}

        data = get_json(url, params=params)
        if not data:
            break

        items = data.get("items", [])
        print(f"Retrieved {len(items)} playlists at offset={offset}")
        playlists.extend(items)

        if len(items) < limit:
            break

        offset += limit
        time.sleep(0.2) 

    print(f"Total playlists from curator: {len(playlists)}\n")
    return playlists

def fetch_artist_batch(batch):
    url = "https://api.spotify.com/v1/artists"
    params = {"ids": ",".join(batch)}
    data = get_json(url, params=params)
    if not data:
        return []
    return data.get("artists", [])


# Build playlist metadata dataframe (with followers, description, image, total_tracks)
def playlists_metadata(raw_playlists, TARGET_CURATOR_NAME, curator_url):
    playlist_meta_rows = []
    for idx, p in enumerate(raw_playlists, start=1):
        pid = p["id"]
        playlist_details = get_json(f"https://api.spotify.com/v1/playlists/{pid}")
        if not playlist_details:
            continue

        followers = (playlist_details.get("followers") or {}).get("total")
        description = playlist_details.get("description")
        images = playlist_details.get("images") or []
        image_url = images[0]["url"] if images else None
        total_tracks = (playlist_details.get("tracks") or {}).get("total")

        playlist_meta_rows.append(
            {
                "playlist_id": pid,
                "playlist_name": playlist_details.get("name"),
                "playlist_url": (playlist_details.get("external_urls") or {}).get("spotify"),
                "followers": followers,
                "description": description,
                "image_url": image_url,
                "total_tracks": total_tracks,
                "public": playlist_details.get("public"),
                "curator_name": TARGET_CURATOR_NAME,
                "curator_url": curator_url,
            }
        )
        time.sleep(0.1)

    return pd.DataFrame(playlist_meta_rows)
     
# Fetch all tracks for a playlist
def fetch_all_tracks_for_playlist(pid):
    all_items = []
    limit = 100
    offset = 0
    while True:
        url = f"https://api.spotify.com/v1/playlists/{pid}/tracks"
        params = {
            "limit": limit,
            "offset": offset,
            "fields": "items(added_at,track(id,name,popularity,explicit,duration_ms,"
                      "album(id,name,release_date),artists(id,name))),total,next"
        }

        data = get_json(url, params=params)
        if not data:
            break

        items = data.get("items", [])
        all_items.extend(items)

        if not data.get("next"):
            break

        offset += limit
        time.sleep(0.15)

    print(f"Total tracks collected for playlist {pid}: {len(all_items)}")
    return all_items

def tracks_data(df_curator_playlists):
    playlist_track_rows = []
    track_rows = []
    print("\nFetching ALL tracks for all playlists...\n")

    for idx, row in df_curator_playlists.iterrows():
        pid = row["playlist_id"]
        pname = row["playlist_name"]

        print(f"[{idx+1}/{len(df_curator_playlists)}] Playlist: {pname} ({pid})")

        items = fetch_all_tracks_for_playlist(pid)
        if not items:
            continue

        for pos, item in enumerate(items):
            track = item.get("track")
            if not track or not track.get("id"):
                continue

            tid = track["id"]

            playlist_track_rows.append(
                {
                    "playlist_id": pid,
                    "track_id": tid,
                    "position": pos,
                    "added_at": item.get("added_at"),
                }
            )

            album = track.get("album") or {}
            artists = track.get("artists") or []

            track_rows.append(
                {
                    "track_id": tid,
                    "track_name": track.get("name"),
                    "track_popularity": track.get("popularity"),
                    "explicit": track.get("explicit"),
                    "duration_ms": track.get("duration_ms"),
                    "album_id": album.get("id"),
                    "album_name": album.get("name"),
                    "album_release_date": album.get("release_date"),
                    "artist_ids": [a.get("id") for a in artists if a.get("id")],
                    "artist_names": [a.get("name") for a in artists if a.get("name")],
                }
            )

        print(f"Finished playlist '{pname}' with {len(items)} track entries.\n")
        time.sleep(0.3)

    df_playlist_tracks = pd.DataFrame(playlist_track_rows)
    df_tracks = pd.DataFrame(track_rows)
    if df_tracks.empty:
        df_tracks = df_tracks.drop_duplicates(subset=["track_id"]).reset_index(drop=True)

    return df_playlist_tracks, df_tracks


# FETCH ARTIST METADATA
def artists_metadata(df_tracks):
    df_art_ids = (
        df_tracks[["track_id", "artist_ids"]]
        .explode("artist_ids")
        .dropna(subset=["artist_ids"])
        .drop_duplicates(subset=["artist_ids"])
        .rename(columns={"artist_ids": "artist_id"})
    )

    artist_ids = df_art_ids["artist_id"].tolist()
    artist_rows = []
    BATCH_SIZE = 50

    for i in range(0, len(artist_ids), BATCH_SIZE):
        batch = artist_ids[i:i + BATCH_SIZE]
        print(f" Fetching artists {i}–{i + len(batch)} / {len(artist_ids)}")
        artists = fetch_artist_batch(batch)

        for a in artists:
            if not a:
                continue
            artist_rows.append(
                {
                    "artist_id": a["id"],
                    "artist_name": a.get("name"),
                    "artist_url": (a.get("external_urls") or {}).get("spotify"),
                    "artist_followers": (a.get("followers") or {}).get("total"),
                    "artist_popularity": a.get("popularity"),
                    "artist_genres": a.get("genres", []),
                }
            )

        time.sleep(0.3)

    return pd.DataFrame(artist_rows).drop_duplicates(subset=["artist_id"]).reset_index(drop=True)

# Build dataset
def build_final_dataset(df_playlist_tracks, df_tracks, df_artists, df_curator_playlists, TARGET_CURATOR_NAME, curator_url):
    df_merge = df_playlist_tracks.merge(
        df_tracks[["track_id", "artist_ids"]],
        on="track_id",
        how="left"
    )

    df_merge = df_merge.explode("artist_ids").rename(columns={"artist_ids": "artist_id"})

    df_merge = df_merge.merge(
        df_artists,
        on="artist_id",
        how="left"
    )

    playlist_profile_rows = []

    for pid, chunk in df_merge.groupby("playlist_id"):
        pmeta = df_curator_playlists[df_curator_playlists["playlist_id"] == pid].iloc[0]
        
        genres = [
            g for g in chunk["artist_genres"].dropna().explode().tolist()
            if isinstance(g, str) and g.strip() != ""
        ]

        all_genres = sorted(set(genres)) if genres else []
        genre_counter = Counter(genres)
        diversity = len(all_genres)
        unique_artists = chunk["artist_id"].nunique()
        avg_artist_popularity = chunk["artist_popularity"].dropna().mean()
        avg_artist_followers = chunk["artist_followers"].dropna().mean()

        playlist_profile_rows.append(
            {
                # Curator info
                "curator_name": TARGET_CURATOR_NAME,
                "curator_url": curator_url,

                # Playlist metadata
                "playlist_id": pid,
                "playlist_name": pmeta["playlist_name"],
                "playlist_url": pmeta["playlist_url"],
                "followers": pmeta["followers"],
                "total_tracks": pmeta["total_tracks"],
                "description": pmeta["description"],
                "image_url": pmeta["image_url"],
                "public": pmeta["public"],

                # GENRE ANALYTICS
                "playlist_genres": all_genres,        
                "genre_histogram": genre_counter,     
                "genre_diversity": diversity,        

                # ARTIST ANALYTICS
                "unique_artists": unique_artists,
                "avg_artist_popularity": avg_artist_popularity,
                "avg_artist_followers": avg_artist_followers,
            }
        )


    return pd.DataFrame(playlist_profile_rows)



# [   {'curator_name': ' ' ,'curator_url': ' '}
#     {'curator_name': ' ' ,'curator_url': ' '}
#     {'curator_name': ' ' ,'curator_url': ' '}
# ]
# main flow 
def driver_code(curators):
    for curator in curators:
        TARGET_CURATOR_NAME = curator['curator_name']
        curator_url = curator['curator_url']
        curator_id = curator_url.rstrip("/").split("/")[-1]

        print(f"🎯 Curator selected: {TARGET_CURATOR_NAME}")
        print(f"👤 curator_id: {curator_id}")
        print(f"🔗 curator_url: {curator_url}\n")

        raw_playlists = fetch_curator_playlists(curator_id, TARGET_CURATOR_NAME)
        
        # Ignore the curators who does not have any playlists or deleted them 
        if not raw_playlists:
            print('Curator does not have any playlist')
            continue

        df_curator_playlists = playlists_metadata(raw_playlists, TARGET_CURATOR_NAME, curator_url)
        df_playlist_tracks, df_tracks = tracks_data(df_curator_playlists)
        
        if df_tracks.empty or df_playlist_tracks.empty:
            print('Curator does not have any tracks in their playlist!')
            continue

        df_artists = artists_metadata(df_tracks)
        df_playlist_profiles = build_final_dataset(df_playlist_tracks, df_tracks, df_artists, df_curator_playlists,
                                                   TARGET_CURATOR_NAME, curator_url)
        
        df_playlist_profiles.to_csv(f'data/{TARGET_CURATOR_NAME}.csv', index=False)

