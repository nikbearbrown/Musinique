# Musinique
Musinique

This is a smart way to split the product.

**"The Playlisters"** list sells the **Relationship** (Who do I contact?).
**"The Playlists"** list sells the **Intelligence** (Is this list safe/worth it?).

Based on the raw data you shared and your "Entropy/Churn" value prop, here are the recommended fields for each file to maximize value for an Indie Artist.

### 📄 File 1: The "Playlisters" Database (The Contact List)
*This file is for pitching. It aggregates data by the "Owner."*

| Field Name | Why It Matters to the Artist |
| :--- | :--- |
| **Curator Name** | Who are they? (e.g., "Filtr US", "IndieMono", "Alex") |
| **Contact Method** | **The $$$ Field.** Email, Instagram handle, Twitter, or Submission Form URL found by your bot. |
| **Website/Social URL** | Verification that they are a real entity. |
| **Total Reach** | Sum of followers across *all* their playlists. (Are they a shark or a minnow?) |
| **Playlist Count** | Do they own 1 list or 500? (500 often implies a network/farm). |
| **Primary Genres** | What do they usually curate? (e.g., "Mostly Deep House & Lo-Fi"). |
| **"Indie Friendliness"** | *Calculated:* % of tracks by artists with <10k followers. |
| **Musinique Trust Score** | Your proprietary score. Aggregated rating of their playlists' quality. |

---

### 📄 File 2: The "Playlists" Database (The Analytics)
*This file is for vetting. It is the deep dive into specific lists.*

**1. The Basics (Identification)**
* `Playlist Name`
* `Playlist URL` (Direct link)
* `Curator Name` (Link to File 1)
* `Description` (Often contains hidden contact info or submission rules).

**2. The Metrics (Is it big?)**
* `Follower Count`
* `Track Count` (High track counts >500 often mean "dumping ground").
* `Last Updated` (**Critical:** If it hasn't been updated in 3 months, don't pitch).

**3. The "Musinique Analytics" (Is it real?)**
* `Primary Genre` & `Sub-Genres` (Your detailed mapping).
* `Genre Diversity Score` (Entropy):
    * *Low Score:* "Strictly Techno" (Good/Human).
    * *High Score:* "Techno + Country + Jazz" (Bad/Bot Farm).
* `Avg Artist Popularity` (0-100):
    * If **>80**: They only play Top 40 hits. Don't waste your time pitching.
    * If **<10**: It might be a bot farm playing fake artists.
    * **Sweet Spot (20-60):** Real Indie lists.
* `Avg Artist Followers`: Are the artists on this list famous or unknown?
* `Unique Artist Count`:
    * If a playlist has 50 tracks but only 4 unique artists, it's a scam (boosting specific friends).

### 💡 The Strategy
**Bundle them.**
* Sell **"The Playlisters"** as the **"Black Book"** (The rolodex of contacts).
* Sell **"The Playlists"** as the **"X-Ray Specs"** (The tool to see through the scams).

**Pro Tip:** In your raw data, the field `description` is often messy. I recommend running a quick script to extract emails from the description column into a clean `email_extracted` column. That one column alone justifies the price of the download.



