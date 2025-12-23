from typing import TypedDict, Optional, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class CuratorState(TypedDict):
    curator_name: str
    spotify_url: str
    instagram: Optional[str]
    twitter: Optional[str]
    facebook: Optional[str]
    submission_form: Optional[str]
    any_other_handle: Optional[List[str]]
    needs_scraping: Optional[List[str]]
    potiential_website: Optional[str]
    
    scraped_urls: Optional[List[str]]
    searched_handles: Optional[List[str]]
    search_count: int
    scrape_count: int
    messages: Optional[List[str]]
    missing: Optional[List[str]]


def create_initial_state(curator_name: str, curator_spotify_url: str) -> CuratorState:
    return {
        "curator_name": curator_name,
        "spotify_url": curator_spotify_url,
        "instagram": None,
        "twitter": None,
        "facebook": None,
        "submission_form": None,
        "any_other_handle": None,
        "potiential_website": None,
        
        "needs_scraping": [],
        "scraped_urls": [],
        "search_count": 0,
        "scrape_count": 0,
        "messages": [],
        "searched_handles": [],
        "missing": [],

    }
