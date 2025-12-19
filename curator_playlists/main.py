from fetch_data import driver_code
from genre_mapping import  mapping_genres
import pandas as pd 
import pathlib 


def main(curators):
    # Trigger Pipeline
    # driver_code(curators)

    # Unify all curators csvs
    data_dir = pathlib.Path('data')
    dfs = []
    for f in data_dir.glob('*.csv'):
        dfs.append(pd.read_csv(f))
    df_all = pd.concat(dfs, ignore_index=True)

    # Empty the folder
    for f in data_dir.glob('*.csv'):
        f.unlink()

    # Map genres
    # df = mapping_genres(mapping_df=mapping_df, df=df_all)

    # Save final data 
    df_all.to_csv('data/Playlisters.csv', index=False)

if __name__ == '__main__':
    curators = [
        {'curator_name': 'Indie Folk Central' ,'curator_url': 'https://open.spotify.com/user/ykxuknpdqe4vrfi4lrn2gb76p'}
    ]

    # Load Metadata
    # mapping_df = pd.read_csv('MetaData/MusicGenres_unique.csv')
    main(curators)




