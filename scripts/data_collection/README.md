# Data Collection

Scripts for collecting Spotify playlist data using the Spotify Web API with asynchronous processing.

## Contents

- `main.py` - Main orchestration script for the data collection pipeline
- `data_collection.py` - Core functions for searching and fetching playlist details
- `config.py` - Configuration file for API credentials and search parameters
- `requirements.txt` - Python package dependencies

## Features

- **Keyword-based Search**: Collects playlists based on predefined keywords
- **Async Processing**: Uses asynchronous HTTP requests for faster data fetching
- **Detailed Information**: Retrieves comprehensive playlist metadata including:
  - Playlist name, ID, and URL
  - Curator name and profile URL
  - Follower counts
  - Track counts
  - Descriptions and images
  - Public/private status

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure `config.py` with your Spotify API credentials:
   - Client ID
   - Client Secret
   - Search keywords
   - Rate limiting settings

## Usage

Run the main script to collect and process playlist data:

```bash
python main.py
```

The script will:
1. Search for playlists using configured keywords
2. Fetch detailed information for each playlist
3. Merge and deduplicate data
4. Save results to CSV files

## Output

Generated data files are saved to the `data/` directory:
- `playlists_base.csv` - Initial collection results
- `playlists_final.csv` - Processed and enriched data

## Notes

- Respects Spotify API rate limits with configurable delays
- Uses nest_asyncio for async processing compatibility
- Automatically handles pagination for large result sets
