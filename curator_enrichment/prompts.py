# AGENT_PROMPT = """
# Goal: Extract contact information for the music playlist curator "{curator_name}" from the provided 
# search results or scraped web pages. Focus on finding any point of contact of them.

# Curators might include noisy names & funky symbols [., *, !, etc] in names - be flexible with matching
# and identify that maybe these two people seems the same person. BE LENIENT with name matching. 
# The curator name provided may have typos, spacing issues, only first names or formatting differences. 
# If you feel the search results should realted to 
# Like curtor BIRP! might have search results with just BIRP or BIRP.DJ or BIRP.fm.

# Current data for {curator_name}:
# {current_state}

# Context: The curator is a person who accepts music playlist submissions. The search results or 
# scraped web pages may contain information about their social media profiles, submission forms, 
# and other useful links. I already have the information shown above, and the AI should only update them if 
# it find something that is stronger or more relevant than the previous one.
# It should mark webpages for needs_scraping, if It believe more information can be extracted or better info might 
# be available for what it already have by scraping the webpage. 
# Avoid marking social handles like facebook, instagram, playlists for needs_scraping as they are of no benefit.
# """

# AGENT_PROMPT = """
# Goal: Extract contact information for the music playlist curator {curator_name} from the provided 
# search results or scraped web pages. Focus on finding social media profiles and submission forms.

# Warning: Ensure extracted information is accurate and related to the provided curator.
# Verify the context confirms this is a music curator/playlist creator, not someone else with the same name 
# (e.g., businesses, celebrities, brands, other entities non-music related).
# Curators may include symbols [., *, !, _ etc] in names or might have some name variation in spelling
# be lenient with matching and recognize when name variations refer to the same curator, becuase my data about
# curator might not be of good quality, so you don't have to just rely on exact matches 
# Just make sure that the context provide you enough info that 
# this is music curator.

# Example: BIRP! is a curator name, but maybe we have music pages/handles that says BIRP, BIRP.DJ, 
# or BIRP.fm (A different variation of name), but they seems to be the same person. Take judment like a human 
# thinking step by step.

# Your reasoning process:
# 1. Is this person/entity related to music curation? (If NO, reject regardless of name)
# 2. Does the found name have ANY similarity to what I'm searching for? (phonetic, spelling, abbreviation)
# 3. Do multiple results consistently show the same name variant? (Strong signal it's correct)

# When in doubt, extract the information if the music context is strong. It's better to be lenient than 
# to miss the real curator over minor name differences.

# Current data I have for {curator_name}:
# {current_state}

# Context: I already have the information shown above, and the AI should only update them if 
# it finds something that is stronger or more relevant than the previous one and is related to {curator_name} 
# and music. 
# I should mark webpages for needs_scraping, if I believe more information can be extracted or better info might 
# be available for what I already have by scraping the webpage. 
# Avoid marking social handles like facebook, instagram, playlists for needs_scraping as they are of no benefit.
# """

# AGENT_PROMPT = """
# Goal: Extract contact information for the music playlist curator {curator_name} from the provided 
# search results or scraped web pages. Focus on finding social media profiles and submission forms.

# Warning - Name Matching:
# BE LENIENT with name matching. The curator name provided may have typos, spacing issues, or formatting 
# differences. Think like a human, not a string matcher.

# Your reasoning process:
# 1. Is this person/entity related to music curation? (If NO, reject regardless of name)
# 2. Does the found name have ANY similarity to what I'm searching for? (phonetic, spelling, abbreviation)
# 3. Do multiple results consistently show the same name variant? (Strong signal it's correct)

# When in doubt, extract the information if the music context is strong. It's better to be lenient than 
# to miss the real curator over minor name differences.

# Warning - Verification:
# Ensure extracted information is actually for a music curator/playlist creator, not someone else with 
# a similar name (e.g., businesses, celebrities, non-music entities). Check for music platform presence, 
# playlists, or curator-related content before extracting.

# Current data I have for {curator_name}:
# {current_state}

# Context - Update Rules:
# Only update existing information if you find something more direct, reliable, or recent than what's 
# already there. Mark webpages as needs_scraping only if they likely contain contact forms, emails, 
# or submission guidelines that aren't visible in snippets. Don't mark social media profiles or streaming 
# playlists for scraping.
# """

# AGENT_PROMPT = """
# Task: Extract verified contact links for the music playlist curator "{curator_name}".

# Output only information that clearly belongs to this curator.
# Minor name variations, symbols, or formatting differences are acceptable if context strongly indicates the same curator.

# Current known data:
# {current_state}

# Rules:
# - Prefer official or frequently referenced links.
# - Do NOT guess or infer links without clear evidence.
# - Update a field only if the new value is more specific or clearly better than the existing one.
# - If a webpage likely contains additional contact details, add it to needs_scraping.
# - Do NOT mark social media profile pages (Instagram, Facebook, Spotify) for scraping.

# Return only structured data. No explanations.
# """

# AGENT_PROMPT = """
# Goal: Extract contact information for the music playlist curator "{curator_name}" from the provided 
# search results or scraped web pages. Focus on finding social media profiles and submission forms.

# Warning - Name Matching:
# BE LENIENT with name matching - think like a human researcher, not a string matcher. The curator name 
# may have typos, spacing issues, symbols, or formatting differences.

# Accept variations like:
# - Symbol differences: BIRP! → BIRP → BIRP.DJ → BIRP.fm
# - Stylistic variations that clearly refer to the same curator

# Your reasoning: Does this relate to music curation? Does the name reasonably match? If yes to both, 
# extract it. When in doubt with strong music context, extract rather than reject.

# Current data for {curator_name}:
# {current_state}

# Context - Update Rules:
# Only update existing information if you find something more direct, reliable, or recent. 
# Mark pages for needs_scraping if they likely contain contact forms, emails, or submission guidelines 
# not visible in snippets. Don't mark social media profiles or playlist pages for scraping.
# """

AGENT_PROMPT = """
Goal: Extract contact information for the music playlist curator "{curator_name}" from the provided search results or scraped web pages. Focus on any point of contact: social media, emails, submission forms, websites, bio links, or company affiliations.  

Name Matching & Flexibility: 
- Curator names may appear differently across platforms (typos, spacing, punctuation, symbols, abbreviations, partial names). 
- Be flexible and consider variations as referring to the same curator if context, branding, or Spotify links suggest a match.
- Example: "BIRP!" might appear as "BIRP", "BIRP.DJ", or "BIRP.fm".  

Input Data:
{current_state}

Instructions:
1. **Update existing info only if new findings are stronger, more complete, or more verifiable.**
2. **Extract the following info if found:**
   - Instagram handle & URL
   - Twitter/X handle & URL
   - Facebook page name & URL
   - TikTok handle & URL
   - Official/personal website
   - Submission form / submission link
   - Any other handle 
3. **Mark pages for `needs_scraping` if they may contain deeper info and put them in Any other handle, if realted to curator**
   - Do **not** mark social handles, Spotify playlists, or already-captured links as `needs_scraping`.  
   - Just remeber to be lineant becuase the curator name that I have might appear something else on various platforms
4. Avoid fabricating info. If info is not found, leave it blank or keep existing.  

"""