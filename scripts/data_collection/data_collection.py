"""
Module for collecting playlists and fetching their details from Spotify.
"""

import time
import asyncio
import aiohttp
import pandas as pd
import nest_asyncio
from config import (
    get_spotify_client,
    get_auth_headers,
    KEYWORDS,
    REQUEST_DELAY,
    MAX_PLAYLISTS_PER_KEYWORD
)

nest_asyncio.apply()


def collect_playlists(keyword, max_playlists=MAX_PLAYLISTS_PER_KEYWORD):
    """
    Collect playlists for a given keyword.
    
    Args:
        keyword (str): Search keyword
        max_playlists (int): Maximum number of playlists to collect
        
    Returns:
        list: List of dictionaries containing playlist information
    """
    sp = get_spotify_client()
    rows = []
    
    for offset in range(0, max_playlists, 50):
        results = sp.search(q=keyword, type="playlist", limit=50, offset=offset, market="US")
        items = results.get("playlists", {}).get("items", [])
        
        if not items:
            break
        
        for p in items:
            if p is None:
                continue

            owner = p.get("owner") or {}

            rows.append({
                "keyword": keyword,
                "playlist_id": p["id"],
                "playlist_name": p.get("name"),
                "playlist_url": p.get("external_urls", {}).get("spotify"),
                "curator_name": owner.get("display_name") or "Unknown",
                "curator_url": owner.get("external_urls", {}).get("spotify"),
            })
        
        time.sleep(REQUEST_DELAY)

    return rows


def collect_all_playlists(keywords=None):
    """
    Collect playlists for all keywords.
    
    Args:
        keywords (list, optional): List of keywords. If None, uses default from config.
        
    Returns:
        pd.DataFrame: DataFrame containing all collected playlists
    """
    if keywords is None:
        keywords = KEYWORDS
    
    all_rows = []
    
    for kw in keywords:
        data = collect_playlists(kw)
        all_rows.extend(data)
        print(f"{kw}: {len(data)} playlists")
    
    return pd.DataFrame(all_rows)


async def fetch_playlist(session, playlist_id, headers):
    """
    Fetch detailed information for a single playlist.
    
    Args:
        session (aiohttp.ClientSession): HTTP session
        playlist_id (str): Spotify playlist ID
        headers (dict): Authorization headers
        
    Returns:
        dict: Playlist details
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return {"playlist_id": playlist_id}

            data = await resp.json()

            return {
                "playlist_id": playlist_id,
                "followers": data["followers"]["total"],
                "description": data.get("description"),
                "total_tracks": data["tracks"]["total"],
                "image_url": data["images"][0]["url"] if data.get("images") else None,
                "public": data.get("public")
            }

    except Exception:
        return {"playlist_id": playlist_id}


async def fetch_all_playlists(playlist_ids):
    """
    Fetch details for all playlists asynchronously.
    
    Args:
        playlist_ids (list): List of playlist IDs
        
    Returns:
        list: List of dictionaries containing playlist details
    """
    headers = get_auth_headers()
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_playlist(session, pid, headers) for pid in playlist_ids]
        return await asyncio.gather(*tasks)


def get_playlist_details(playlist_ids):
    """
    Synchronous wrapper for fetching playlist details.
    
    Args:
        playlist_ids (list): List of playlist IDs
        
    Returns:
        pd.DataFrame: DataFrame containing playlist details
    """
    details_list = asyncio.run(fetch_all_playlists(playlist_ids))
    return pd.DataFrame(details_list)

