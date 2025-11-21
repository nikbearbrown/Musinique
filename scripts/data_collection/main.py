"""
Main script for collecting and processing Spotify playlist data.
"""

import os
import pandas as pd
from data_collection import collect_all_playlists, get_playlist_details


def process_playlist_data(df_base, df_details):
    """
    Merge and process playlist data.
    
    Args:
        df_base (pd.DataFrame): Base playlist data from collection
        df_details (pd.DataFrame): Detailed playlist information
        
    Returns:
        pd.DataFrame: Processed and cleaned dataframe
    """
    # Clean playlist IDs
    df_base["playlist_id"] = df_base["playlist_id"].astype(str).str.strip()
    df_details["playlist_id"] = df_details["playlist_id"].astype(str).str.strip()
    
    # Merge base data with details
    df_enriched = df_base.merge(df_details, on="playlist_id", how="left")
    
    # Remove duplicates
    df_unique = df_enriched.drop_duplicates(subset=["playlist_id"]).copy()
    
    # Aggregate keywords per playlist
    df_keywords = (
        df_base.groupby("playlist_id")["keyword"]
          .apply(lambda x: sorted(set(x)))
          .reset_index()
    )
    df_keywords.rename(columns={"keyword": "keywords"}, inplace=True)
    
    # Final merge
    df_final = pd.merge(
        df_unique,
        df_keywords,
        on="playlist_id",
        how="left",
        validate="one_to_one"
    )
    
    # Select final columns
    final_cols = [
        "playlist_id",
        "playlist_name",
        "playlist_url",
        "curator_name",
        "curator_url",
        "followers",
        "total_tracks",
        "description",
        "image_url",
        "public",
        "keywords"
    ]
    
    df_final = df_final[[c for c in final_cols if c in df_final.columns]]
    
    return df_final


def main():
    """
    Main function to collect playlists, fetch details, and process data.
    """
    # Create data directory if it doesn't exist
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    print("Starting playlist collection...")
    
    # Step 1: Collect playlists from keywords
    df_base = collect_all_playlists()
    print(f"\nTotal playlists collected: {len(df_base)}")
    
    # Save base data
    base_path = os.path.join(data_dir, "playlists_base.csv")
    df_base.to_csv(base_path, index=False)
    print(f"Saved {base_path}")
    
    # Step 2: Fetch detailed information
    print("\nFetching playlist details...")
    playlist_ids = df_base["playlist_id"].tolist()
    df_details = get_playlist_details(playlist_ids)
    print(f"Fetched details for {len(df_details)} playlists")
    
    # Step 3: Process and merge data
    print("\nProcessing data...")
    df_final = process_playlist_data(df_base, df_details)
    print(f"Final shape: {df_final.shape}")
    
    # Save final data
    final_path = os.path.join(data_dir, "playlists_final.csv")
    df_final.to_csv(final_path, index=False)
    print(f"Saved {final_path}")
    
    print("\nDone!")
    return df_final


if __name__ == "__main__":
    df_final = main()
    print(f"\nFinal dataset preview:")
    print(df_final.head())
