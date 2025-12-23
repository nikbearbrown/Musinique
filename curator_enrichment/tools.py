import requests
from bs4 import BeautifulSoup
import requests
from typing import List, Dict
import os 
from dotenv import load_dotenv
from config import base_url
from langchain_core.tools import tool
import requests

load_dotenv()

API_KEY = os.getenv('SERP_API_KEY')
CX = os.getenv('CX')

GROQ_API_KEYS = [
    os.getenv('GROQ_API_KEY_1'),
    os.getenv('GROQ_API_KEY_2'),
    os.getenv('GROQ_API_KEY_3'),
    os.getenv('GROQ_API_KEY_4'),
    os.getenv('GROQ_API_KEY_5'),
]

@tool
def google_search(query: str) -> List[Dict]:
    """
    Search Google and return query results.

    Parameters: 
        query (str): The query we need to search for on google (like: curator_X instagram, curator_Y playlists form)
    
    Returns: 
        A list of {title, link, snippet, domain}
    """
    # Your SerpApi key
    api_key = API_KEY
    url = "https://serpapi.com/search.json"

    # Query parameters
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    search_results = []
    if not data.get('organic_results', None):
        return search_results
    
    for item in data['organic_results']:
        search_results.append({
            'title': item.get('title', ''),
            'link': item.get('link', ''),
            'source': item.get('source', ''),
            'snippet': item.get('snippet', ''),
            'snippet_highlighted_words': item.get('snippet_highlighted_words', '')
        })
    
    return search_results

@tool
def scrape_page(url: str) -> str:
    """
    Scrape a webpage and return cleaned visible text.
    Never raises — always returns a string.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CuratorBot/1.0)"
    }

    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=8,          # lower timeout = faster failures
            allow_redirects=True
        )

        # Handle non-200 responses
        if response.status_code >= 400:
            return f"[SCRAPE_FAILED] HTTP {response.status_code} for {url}"

    except requests.exceptions.Timeout:
        return f"[SCRAPE_FAILED] Timeout while fetching {url}"

    except requests.exceptions.RequestException as e:
        return f"[SCRAPE_FAILED] Request error for {url}: {str(e)}"

    # ---- Parse HTML safely ----
    try:
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "iframe"]):
            tag.decompose()

        # Replace links with readable format
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            href = a["href"]
            if text:
                a.replace_with(f"{text} [{href}]")

        texts = []
        for line in soup.get_text(separator="\n").splitlines():
            line = line.strip()
            if line:
                texts.append(line)

        content = "\n".join(texts)

        # Truncate aggressively (VERY IMPORTANT)
        return content[:8000]

    except Exception as e:
        return f"[SCRAPE_FAILED] HTML parsing error for {url}: {str(e)}"


@tool
def filter_search_results(items, entity_name):
    """
    Filter Google search results to remove noise.
    """
    entity = entity_name.lower()

    tokens = [t.lower() for t in entity.split() if len(t) > 2]
    

    filtered = []

    for item in items:
        title = item.get("title", "").lower() 
        snippet = item.get("snippet", "").lower() 
        link = item.get("link", "").lower() 
        
        if (tokens[0] in title or 
            tokens[0] in link):
            filtered.append(item)
        
        elif (entity in title or 
            entity in link):
            filtered.append(item)

    return filtered
