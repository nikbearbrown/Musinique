## Combined Vote Calculation

Each track is scored using a **Combined Vote** to capture both its **genre diversity** and **curator usage**.

### Inputs

* **Genre Appearance**
  Each track receives one vote for every genre associated with its artist(s). Multiple genres per artist mean multiple genre votes per track.

* **Playlist Appearance**
  Counts **each playlist** in which a track appears, even if multiple playlists belong to the same curator.
  Example: If a song appears in 10 playlists from one curator, the playlist appearance vote is **10**.

### Formula

```
combined_vote = genre_appearance × playlist_appearance
```

## Musinique Focus Score Calculation

The **Musinique Focus Score** (0-100) measures how niche/focused a playlist is using three components:

**1. Genre Breadth Score (45% weight)**
- Rewards playlists with fewer primary genres
- 100 points for 1 genre, decreases logarithmically to 0 at 50+ genres

**2. Genre Density Score (30% weight)**
- Measures average tracks per genre
- 100 points at 80+ tracks/genre, scales linearly down to 0 at 5 tracks/genre

**3. Artist Focus Score (25% weight)**
- Rewards artist repetition (lower unique artist ratio)
- 100 points when ≤30% artists are unique, decreases to 0 when all artists are unique

**Final Score**: `(0.45 × S1) + (0.30 × S2) + (0.25 × S3)`

Higher scores indicate more focused, niche playlists. Lower scores suggest broader, more diverse curation.
