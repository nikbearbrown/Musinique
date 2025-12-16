AGENT_PROMPT = """
Goal: Extract contact information for the music playlist curator "{curator_name}" from the provided 
search results or scraped web pages. Focus on finding "{curator_name}" social media profiles and submission forms 
used for accepting music playlist submissions.

Return format: Return a JSON object with the following fields. Only include URLs that are directly 
visible in the content and verified to belong to {curator_name}:
{{   
    "instagram": "URL or null",  
    "twitter": "URL or null",  
    "facebook": "URL or null", 
    "submission_form": "URL/link or null" (submission forms),
    "other_links": ["URL1", "URL2"] or [],  
    "needs_scraping": ["URL1", "URL2"] or []
}}

Warning: The AI should ensure that the extracted information is accurate, related to the specific {curator_name}, 
and not randomly associated with any person, business, or entity. It must avoid creating fictional links 
or hallucinating information, and only provide true and contextually relevant data. 

Current data for {curator_name}:
{current_state}

Context: The curator is a person who accepts music playlist submissions. The search results or 
scraped web pages may contain information about their social media profiles, submission forms, 
and other useful links. I already have the information shown above, and the AI should only update them if 
it find something that is stronger or more relevant than the previous one and is related to {curator_name} 
and music. (Since curators are linked to music)
Before extracting any social media URL, verify that the account/page name actually matches "{curator_name}" or is clearly 
operated by them. Do not extract URLs for other people mentioned in the content other than {curator_name}.
I should mark webpages for needs_scraping, if I believe more information can be extracted or better info might 
be available for what I already have by scraping the webpage. 
Avoid marking social handles like facebook, instagram, playlists for needs_scraping as they are of no benefit.

Analyze this content:
"""
