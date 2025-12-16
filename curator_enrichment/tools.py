import requests
from bs4 import BeautifulSoup
import requests
from typing import List, Dict
import os 
from dotenv import load_dotenv
from config import base_url
from langchain_core.tools import tool

load_dotenv()

API_KEY = os.getenv('API_KEY')
CX = os.getenv('CX')

@tool
def google_search(query: str) -> List[Dict]:
    """
    Search Google and return query results.

    Parameters: 
        query (str): The query we need to search for on google (like: curator_X instagram, curator_Y playlists form)
    
    Returns: 
        A list of {title, link, snippet, domain}

    """

    params = {
        'key': API_KEY,
        'cx': CX,
        'q': query,
        "gl": "US",       
        "hl": "en"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    results = []
    for item in data.get('items', []):
        results.append({
            'title': item.get('title', ''),
            'link': item.get('link', ''),
            'snippet': item.get('snippet', '')
        })


    return results

@tool
def scrape_page(url: str)-> str:
    """
    Scrape a webpage and return content of th web page.

    Parameters: 
        url (str): A url whose web content we need to scrape

    Returns: 
        A str of the scraped content
    """
    
    headers = {"User-Agent": "Mozilla/5.0 (compatible; CuratorBot/1.0)"}
    resposne = requests.get(url=url, headers=headers, timeout=10)
    soup = BeautifulSoup(resposne.text, 'html.parser')

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    for a in soup.find_all("a", href=True):
        text = a.get_text()
        url = a['href']

        if text:
            a.replace_with(f'{text} [{url}]')


    texts = []
    for line in soup.get_text(separator='\n').splitlines():
        if line.strip():
            texts.append(line.strip())

    return "\n".join(texts)

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
