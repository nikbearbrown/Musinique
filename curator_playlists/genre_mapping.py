import pandas as pd
from utils import map_playlist_genres
from collections import Counter

def mapping_genres(mapping_df, df):
    mapped_list = []
    unmapped_list = []
    for idx, row in df.iterrows():
        raw_genres = row["playlist_genres"]
        mapped, unmapped = map_playlist_genres(raw_genres, mapping_df=mapping_df)

        mapped_list.append(mapped)
        unmapped_list.append(unmapped)

    df["mapped_parent_genres"] = mapped_list
    df["unmapped_genres"] = unmapped_list
    df["parent_genre_histogram"] = None
    df["genre_diversity_parent"] = None
    df["full_parent_genre_list"] = None

    for idx, row in df.iterrows():
        parents = row["mapped_parent_genres"]
        if not isinstance(parents, list):
            parents = []
        
        counter = Counter(parents)
        df.at[idx, "parent_genre_histogram"] = counter
        df.at[idx, "genre_diversity_parent"] = len(counter)
        df.at[idx, "full_parent_genre_list"] = sorted(list(counter.keys()))

    df_sample = df[[
        "curator_name", "curator_url", "playlist_name", "playlist_url", "followers", "total_tracks",
        "description", 'unique_artists', 'avg_artist_popularity', 'avg_artist_followers',
        'mapped_parent_genres', 'parent_genre_histogram','genre_diversity_parent', 
        "playlist_genres", "genre_histogram", "genre_diversity",
    ]]

    df_sample.rename(columns={
        "mapped_parent_genres": "primary_genres",
        "genre_diversity_parent": "primary_genre_diversity",
        "playlist_genres": "all_genres",
        "genre_diversity": "all_genre_diversity"  
    }, inplace=True)

    df_sample.drop(columns=['parent_genre_histogram', 'genre_histogram'], inplace=True)

    return df_sample


