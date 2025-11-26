# Spotify URL Validator

Python scripts that validate Spotify playlist and profile URLs from a CSV file using Playwright web automation with anti-bot detection measures.

## Available Scripts

- **`spotify_validator.py`** - Single-threaded validator (slower, sequential processing)
- **`multiprocessing-spotify-validator.py`** - Multi-threaded validator (faster, parallel processing) ⚡

## Features

- ✅ Validates Spotify playlist URLs
- ✅ Validates Spotify profile/user URLs  
- ✅ Human-like browsing behavior (random delays, mouse movements, scrolling)
- ✅ Anti-bot detection measures
- ✅ Processes CSV files with multiple columns
- ✅ Adds validation results without modifying existing data
- ✅ Multi-process support for faster validation (multiprocessing version)

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

**For Single-threaded Version (`spotify_validator.py`):**

Edit the file paths at the bottom:

```python
INPUT_FILE = "spotify_data.csv"              # Your input file
OUTPUT_FILE = "spotify_data_validated.csv"   # Output file name
```

**For Multiprocessing Version (`multiprocessing-spotify-validator.py`):**

Edit the configuration at the bottom:

```python
INPUT_FILE = "spotify_data_complete.csv"      # Your input file
OUTPUT_FILE = "processed/spotify_data_validated.csv"  # Output file name
NUM_PROCESSES = 16                            # Number of parallel processes (adjust based on CPU cores)
SAVE_INTERVAL = 100                           # Save progress after every N results
```

### 3. Run the Script

**Single-threaded (slower, more stable):**
```bash
python spotify_validator.py
```

**Multiprocessing (faster, recommended for large datasets):**
```bash
python multiprocessing-spotify-validator.py
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

### Choosing Between Scripts

**Use `spotify_validator.py` when:**
- Processing small datasets (< 100 URLs)
- You want to see the browser window (debugging)
- System has limited CPU cores
- Stability is more important than speed

**Use `multiprocessing-spotify-validator.py` when:**
- Processing large datasets (hundreds or thousands of URLs)
- Speed is important
- System has multiple CPU cores (4+)
- You want automatic progress saving

### Multiprocessing Configuration

Adjust these settings in `multiprocessing-spotify-validator.py`:

```python
NUM_PROCESSES = 16      # Set to your CPU core count (use 1-2x cores)
SAVE_INTERVAL = 100     # How often to save progress (lower = more frequent saves)
```

To check your CPU cores:
```bash
# macOS/Linux
sysctl -n hw.ncpu

# Python
python -c "import os; print(os.cpu_count())"
```

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
csv_processing/
├── venv/                                      # Virtual environment (generated)
├── requirements.txt                           # Python dependencies
├── spotify_validator.py                       # Single-threaded validator
├── multiprocessing-spotify-validator.py       # Multi-process validator ⚡
├── spotify_data.csv                          # Your input file
├── spotify_data_complete.csv                 # Large input file example
├── spotify_data_validated.csv                # Output file (generated)
├── processed/                                # Validated output directory
│   └── spotify_data_validated.csv           # Multiprocessing output
├── change-log.md                             # Version history
└── README.MD                                 # This file
```

## Performance Comparison

| Script | Processing Speed | CPU Usage | Memory | Best For |
|--------|-----------------|-----------|---------|----------|
| `spotify_validator.py` | ~5-10 sec/URL | Low (1 core) | Low | Small datasets |
| `multiprocessing-spotify-validator.py` | ~1-2 sec/URL | High (multi-core) | Medium | Large datasets |

**Example:** Processing 1000 URLs
- Single-threaded: ~2-3 hours
- Multiprocessing (16 cores): ~20-30 minutes

## Notes

- Both scripts run in **non-headless mode** by default (you'll see the browser)
- Single-threaded: ~5-10 seconds per URL (due to human-like delays)
- Multiprocessing: ~1-2 seconds per URL (parallel processing)
- Large CSV files will take considerable time (use multiprocessing version for speed)
- Scripts preserve all original data - only add new columns
- Multiprocessing version includes automatic progress saving
- Output is saved to `processed/` directory when using multiprocessing script

## Multiprocessing Features

The `multiprocessing-spotify-validator.py` script includes:

- **Parallel Processing**: Processes multiple URLs simultaneously using multiple CPU cores
- **Progress Tracking**: Real-time progress updates with ETA
- **Auto-Save**: Periodically saves results (configurable interval)
- **Error Recovery**: Continues processing even if individual URLs fail
- **Statistics**: Detailed completion stats (total time, average time per URL)
- **Output Directory**: Automatically saves to `processed/` folder
