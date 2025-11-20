# Spotify URL Validator (11/05/2025)

A Python script that validates Spotify playlist and profile URLs from a CSV file using Playwright web automation with anti-bot detection measures.

## Features

- ✅ Validates Spotify playlist URLs
- ✅ Validates Spotify profile/user URLs  
- ✅ Human-like browsing behavior (random delays, mouse movements, scrolling)
- ✅ Anti-bot detection measures
- ✅ Processes CSV files with multiple columns
- ✅ Adds validation results without modifying existing data

## Requirements

- Python 3.11 or 3.12 (recommended)
- macOS, Windows, or Linux

## Installation

### 1. Clone or Download

Download the project files to your computer and navigate to the directory:

```bash
cd spotify-validator
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Install Playwright Browsers

```bash
playwright install
```

This downloads Chromium, Firefox, and WebKit browsers (~300MB).

## Usage

### 1. Prepare Your CSV File

Place your CSV file (e.g., `spotify_data.csv`) in the project directory. The CSV should have a column named `spotify_url` with Spotify links.

**Example CSV format:**
```csv
curator,curator_email,spotify_url,followers
Felix,felix@example.com,https://open.spotify.com/playlist/1DRpqg3Vlub1gKMWN14gCg,8.4K
John,john@example.com,https://open.spotify.com/user/johnsmith,2.5K
```

### 2. Update Script Configuration

Edit `spotify_validator.py` and update the file paths at the bottom:

```python
INPUT_FILE = "spotify_data.csv"              # Your input file
OUTPUT_FILE = "spotify_data_validated.csv"   # Output file name
```

### 3. Run the Script

```bash
python spotify_validator.py
```

### 4. View Results

The script creates a new CSV file with two additional columns:
- `is_playlist`: Shows "valid playlist" or "invalid playlist"
- `is_profile`: Shows "valid profile link" or "invalid profile link"

## Output Examples

| spotify_url | is_playlist | is_profile |
|------------|-------------|------------|
| https://open.spotify.com/playlist/abc123 | valid playlist | |
| https://open.spotify.com/user/john | | valid profile link |
| https://open.spotify.com/playlist/invalid | invalid playlist | |

## Anti-Bot Features

The script includes several features to appear more human-like:

- 🎯 Random delays between requests (3-8 seconds)
- 🖱️ Random mouse movements
- 📜 Human-like scrolling patterns
- ⏸️ Long breaks every 5-10 requests (15-30 seconds)
- 🎭 Browser fingerprint masking
- 🌐 Realistic headers and user agent

## Troubleshooting

### Browser Not Found Error

If you see `Executable doesn't exist` error:

```bash
playwright install
```

### Python Version Issues

If you're on Python 3.13+, downgrade to Python 3.11:

```bash
brew install python@3.11
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

### Permission Errors

Try installing browsers with sudo:

```bash
sudo playwright install
```

### Rate Limiting

If Spotify blocks your requests:
- Increase delay times in the script
- Run script during off-peak hours
- Process fewer URLs per session

## Configuration Options

### Headless Mode

To run browser invisibly (faster but less human-like), change in script:

```python
browser = p.chromium.launch(headless=True)
```

### Adjust Delays

Modify timing in the script:
- `time.sleep(random.uniform(3.0, 8.0))` - Change range for request delays
- `time.sleep(random.uniform(15.0, 30.0))` - Change break duration

## Project Structure

```
spotify-validator/
├── venv/                          # Virtual environment (generated)
├── requirements.txt               # Python dependencies
├── spotify_validator.py           # Main script
├── spotify_data.csv              # Your input file
├── spotify_data_validated.csv    # Output file (generated)
└── README.md                      # This file
```

## Notes

- The script runs in **non-headless mode** by default (you'll see the browser)
- Processing time: ~5-10 seconds per URL (due to human-like delays)
- Large CSV files will take considerable time
- Script preserves all original data - only adds new columns
