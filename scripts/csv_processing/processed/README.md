# Processed Data

This directory contains validated and processed Spotify data files.
- spotify_data_validated.csv - complete file after processing
- spotify_valid_playlist.csv - filtered data with only valid playlists
- spotify_valid_playlist.csv - filtered data with only valid profiles

## Contents

- `spotify_data_validated.csv` - CSV file with validated Spotify URLs

## Description

Files in this folder have been processed through the URL validation pipeline and include:

### Additional Validation Columns

- `is_playlist` - Validation status for playlist URLs
  - "valid playlist" - URL points to an active Spotify playlist
  - "invalid playlist" - URL is broken or playlist doesn't exist
  - Empty if not a playlist URL

- `is_profile` - Validation status for profile URLs
  - "valid profile link" - URL points to an active Spotify user profile
  - "invalid profile link" - URL is broken or profile doesn't exist
  - Empty if not a profile URL

## Validation Process

Data in this folder has been validated using:
- Playwright browser automation
- Anti-bot detection measures (random delays, mouse movements)
- Multi-layered content verification
- Error page detection

## Notes

- All original data columns are preserved
- Validation columns are appended to existing data
- Processing time depends on dataset size (~5-10 seconds per URL)
