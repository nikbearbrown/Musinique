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

# Musinique Curator Intelligence Database 🎵🤖

### 25,000+ Playlisters. Analyzed. Verified. Contactable.

**Stop guessing. Start pitching.**

The Musinique Curator Intelligence Database is a comprehensive dataset designed for Independent Artists, Labels, and Managers. We used proprietary AI to analyze over 25,000 Spotify curators, distinguishing **Real Human Taste** from **Bot Farms** and **Pay-for-Placement Scams**.

---

## 🚀 The Mission: Humans + AI
Most playlist promotion services are opaque "black boxes." You pay money, and you hope for streams.

We believe artists deserve **Raw Data**.
We do not sell placements. We sell the intelligence you need to make your own decisions. By analyzing **Entropy (Genre Diversity)** and **Churn (Turnover Rates)**, we give you the "X-Ray Specs" to see which playlists are safe for your career and which will hurt your algorithmic reputation.

---

## 📂 The Dataset Structure

The full database is split into three relational files to help you target the right partners.

### 1. The Playlisters (The Contact List)
*Targeting the human behind the lists. Does this curator have a consistent "sound" across their catalog?*

| Field | Description |
| :--- | :--- |
| `curator_name` | The name of the brand or individual. |
| `contact_method` | **The Priority Field.** Extracted Emails, Instagram handles, X/Twitter, or Web Submission forms. |
| `total_reach` | Total follower count across all their playlists. |
| `playlist_count` | Number of lists they manage. |
| `primary_genres` | The broad musical categories they cover (e.g., "Deep House, Lo-Fi, Jazz"). |
| **`avg_focus_score`** | **(High = Good)**. The average consistency of their playlists. High scores mean they are "Tastemakers" with distinct, focused lists. Low scores imply they mix random genres (a sign of "pay-for-play" farms). |

### 2. The Playlists (The Content Analysis)
*Vetting specific lists for quality and fit.*

| Field | Description |
| :--- | :--- |
| `playlist_name` | Title of the specific list. |
| `primary_genre` | The dominant genre mapped to our taxonomy. |
| `sub_genres` | Detailed tags (e.g., "Acid Techno", "Delta Blues", "Kawaii Future Bass"). |
| `track_count` | Total songs. Lists with >1,000 tracks are often "dumping grounds." |
| `last_updated` | Date of last addition. Filters out dead lists. |
| **`musinique_focus_score`** | **(0-100 Scale)**. How consistent is the vibe? <br>• **Score 80-100 (High):** Hyper-focused. (e.g., "Strictly 90s Boom Bap"). <br>• **Score 40-70 (Mid):** Normal human variety. <br>• **Score < 20 (Low):** **⚠️ Red Flag.** The list is chaotic (e.g., mixing Metal, K-Pop, and Country). |
| `avg_artist_popularity` | (0-100). If >80, they only play Top 40 hits. If <10, risk of bot-generated artists. |

### 3. The Churn (The Behavioral Analysis)
*Detecting "Pay-for-Placement" scams through time-series data.*

| Field | Description |
| :--- | :--- |
| `weekly_turnover_rate` | What % of the playlist was replaced in the last 7 days? |
| **`avg_song_retention`** | Average days a song stays on the list. <br>• **7 Days Exact:** 🚩 **Red Flag** (Likely selling 1-week spots). <br>• **28+ Days:** ✅ **Green Flag** (Healthy human curation). |
| `growth_pattern` | Flag for "Organic Growth" vs. "Bot Spikes" (instant follower gains). |
| `rapid_drop_flag` | Boolean. True if songs consistently drop off exactly after a paid interval. |

---

## 🧠 Methodology: The Musinique Focus Score

We use a statistical approach to calculate "Playlist Entropy"—a measure of sonic chaos. To make this easy to understand, we convert it into a **0-100 Focus Score**, where **Higher is Better**.

### How we calculate it:
We analyzed thousands of playlists to find the "normal" amount of genre variety.
* **The Average Playlist** has ~9 primary genres (Standard Deviation: 2.5).
* **A Focused Playlist (Good)** has 3–6 genres. This gets a high score.
* **A Chaotic Playlist (Bad)** has 14+ genres. This is a statistical outlier (Top 7% of chaos).

**Why does this matter?**
A real human DJ might like *Death Metal* and *K-Pop*, but they would never put them in the same playlist.
A **Bot Farm**, however, accepts money from *anyone* and dumps all the songs into the same list to maximize profit.
* **High Focus Score (Low Diversity):** Safe. Human.
* **Low Focus Score (High Diversity):** Risky. Likely a Bot Farm.

---

## 🌍 Supported Genres
We have identified curators for thousands of specific sub-genres, including but not limited to:

<details>
<summary><strong>Click to view covered genres</strong></summary>

* **Avant-Garde:** Drone, Glitch, Noise, Outsider Music...
* **Blues:** Delta Blues, Chicago Blues, Swamp Blues...
* **Electronic:** Amapiano, Phonk, Vaporwave, Acid Techno, DnB...
* **Metal:** Djent, Blackgaze, Sludge, Industrial...
* **Folk:** Anti-Folk, Neofolk, Sea Shanties...
* **Hip Hop:** Boom Bap, Drill, Trap, Lo-Fi, Phonk...
* **Pop:** Hyperpop, City Pop, Shibuya-kei...
* **Jazz:** Hard Bop, Acid Jazz, Gypsie Jazz...
* **And thousands more.**

</details>

---

## 📥 How to Access
This dataset is available exclusively through **Musinique**.

* **Get the Data:** [Link to Gumroad / Musinique Product Page]
* **Join the Waitlist:** [Link to Waitlist]

---

## ⚖️ Legal & Disclaimer
*Musinique, LLC provides this data "as is" for informational purposes only. We are not accusing any specific playlist of fraud. Our "Trust Scores" and "Bot Flags" are probabilistic estimates based on public data patterns (Entropy and Churn), not definitive legal judgments. We empower artists to interpret this data and make their own informed decisions.*

---

## 🤖 About Musinique
**Humans + AI + Music.**
Musinique builds tools for Indie musicians, poets, and songwriters to be more creative and productive. We believe that great music comes from the partnership of human soul and artificial intelligence.

* **Website:** [musinique.com](https://musinique.com)
* **YouTube:** [@humanitariansai](https://www.youtube.com/@humanitariansai)
* **Lyrical Literacy:** Our non-profit initiative using music + AI for education.



