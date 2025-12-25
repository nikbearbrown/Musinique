
# 🎵 Musinique Curator Database (Gumroad Launch)

## Project Overview
**Mission:** To provide independent artists with a clean, verified, and "bot-checked" database of playlist curators, saving them hundreds of hours of manual research.

**The Hook:** *"Humans make music. Bots check data."*
Artists should be in the studio, not spreadsheet hell. We used our bot ecosystem to verify 5,800+ playlists so they don't have to.

---

## 📂 Folder Structure

```text
Gumroad/
├── assets/                  # Marketing visuals (Puppets, Screen recordings)
├── data/                    # The CSV files (Input and Output)
│   ├── raw/                 # Original data (Do not edit)
│   └── formatted/           # Cleaned files ready for sale
├── scripts/                 # Python tools for data processing
├── copy/                    # Sales descriptions and Ad scripts
└── README.md                # This file

```

---

## 🛠 The Data Pipeline

We do not sell raw scrapes. We sell **Formatted & Verified** data. All scripts must be run before uploading new files to Gumroad.

### 1. Formatting Scripts (Run First)

These scripts strip out code syntax (`['Genre']`), fix URL columns, and calculate metrics.

* **`scripts/format_playlisters.py`**: Cleans the curator list (84 rows). Fixes the "Contact Method" column.
* **`scripts/format_playlists.py`**: Cleans the playlist list (5,800 rows). Formats dates, rounds Focus Scores, and cleans genre tags.

### 2. Sampling Scripts (Run Second)

These generate the "Free Tier" files using **Stratified Sampling** (ensuring every genre is represented).

* **`scripts/sample_playlisters_stratified.py`**: Picks 15 diverse curators (1 from each genre category).
* **`scripts/create_stratified_sample.py`**: Picks 1,000 diverse playlists (guaranteeing niche genres like Gothic/Metal are included).

**Usage:**

```bash
# Run from the command line
python scripts/format_playlisters.py data/raw/Playlisters.csv
python scripts/format_playlists.py data/raw/Playlists.csv
# (Then run sampling scripts on the formatted output)

```

---

## 📦 Product Definitions (Gumroad)

### Product 1: The Lead Magnet (Free)

* **Name:** The Indie Playlister Starter Pack (Free Sample)
* **Content:** 15 Curators + 1,000 Playlists (Stratified Sample).
* **Price:** $0+ (Pay what you want).
* **Goal:** Capture emails. Prove that our data includes niche genres and isn't just "Pop."

### Product 2: The Core Product (Paid)

* **Name:** The Complete Curator Database (5,800+ Verified Playlists)
* **Content:** All 84 Curators + All 5,800+ Playlists.
* **Price:** **$25.00**
* **Goal:** Revenue. Positioned as an "Impulse Buy" that saves 36 weeks of work.

---

## 📢 Marketing Strategy & Assets

### The Core Pitch: "The Impossible Math"

We justify the price by calculating the time cost of manual research.

> *To manually verify 5,800 playlists (checking every artist's genre) would take a human **1,450 hours**. It takes our bots seconds. You are buying 36 weeks of your life back for $25.*

### Video Ad Concepts

We use **Stop-Motion Puppets** to separate the "Artist" (Human) from the "Data" (Bot).

| Ad Name | Target Audience | Visual Hook | Key Message |
| --- | --- | --- | --- |
| **"The Speed"** | Efficiency Lovers | **Prince Puppet** | "You should be playing music, not doing data entry. Bots check data." |
| **"The Focus"** | Serious Songwriters | **Joni Mitchell Puppet** | "Why is your Folk song on a Death Metal playlist? Check the Focus Score." |

### Key Definitions for Customers

* **Focus Score:** Our proprietary metric.
* *High (Green):* Consistent Genre (Safe to pitch).
* *Low (Red):* Messy/Mixed Genre (Risky to pitch).


* **Verification:** We define "Verified" as *scanning the artists inside the list*, not just reading the playlist title.

---

## ⚠️ "Bot Disclaimer" Policy

*To manage expectations and reduce refunds, this text must appear on the sales page:*

> **A Note on Automation:** While we make every effort to be accurate, **these are bots doing the work.** Algorithms lack human intuition. If a playlist looks like a great fit in the data, we always recommend clicking the link and taking a look for yourself before pitching.

---

## 🔄 Maintenance & Roadmap

* **Weekly Scans:** We re-run the bot verification weekly to fight "Data Entropy" (broken links).
* **Churn Data (v2.0):** Future update will include metrics on how often playlists add/remove songs.

