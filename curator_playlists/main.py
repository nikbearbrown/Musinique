from fetch_data import driver_code
from genre_mapping import  mapping_genres
import pandas as pd 
import pathlib 
from config import CURATOR_START_INDEX, CURATOR_END_INDEX
from utils import musinique_focus_score

def main(curators, mapping_df):
    # Trigger Pipeline
    driver_code(curators)

    # Unify all curators csvs
    data_dir = pathlib.Path('final_data')
    dfs = []
    for f in data_dir.glob('*.csv'):
        dfs.append(pd.read_csv(f))
    df_all = pd.concat(dfs, ignore_index=True)

    # Empty the folder
    for f in data_dir.glob('*.csv'):
        f.unlink()

    # Map genres
    df = mapping_genres(mapping_df=mapping_df, df=df_all)

    # Score calculation 
    df['musinique_focus_score'] = df.apply(musinique_focus_score, axis=1)

    # Save final data 
    df.to_csv('data/Playlisters.csv', index=False)

if __name__ == '__main__':
    raw_data = pd.read_csv(pathlib.Path('../scripts/raw_data/df_musinque.csv'))
    curators = raw_data[['curator_name', 'curator_url']][CURATOR_START_INDEX: CURATOR_END_INDEX].drop_duplicates().to_dict(orient='records')
    
    # Load Metadata
    mapping_df = pd.read_csv(pathlib.Path('../MetaData/MusicGenres_unique.csv'))
    main(curators, mapping_df)




