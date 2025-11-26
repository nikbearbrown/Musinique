# Scripts

This directory contains automation scripts for collecting, processing, and validating Spotify playlist data.

## Directory Structure

```
scripts/
├── data_collection/     # Spotify API data collection scripts
├── raw_data/           # Raw collected data files
└── csv_processing/     # Data validation and processing scripts
```

## Overview

The scripts folder contains three main components:

1. **Data Collection** - Scripts to collect Spotify playlist information using the Spotify API
2. **Raw Data** - Storage for initial data collection results
3. **CSV Processing** - Tools for validating and processing Spotify URLs with anti-bot detection

## Workflow

1. Collect playlist data using the `data_collection` scripts
2. Raw data is stored in `raw_data` folder
3. Process and validate data using `csv_processing` scripts
4. Validated output is generated in the `csv_processing` folder
