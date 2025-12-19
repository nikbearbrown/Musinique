from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from tools import google_search, scrape_page, filter_search_results
from state import CuratorState, create_initial_state
from prompts import AGENT_PROMPT
from pydantic import BaseModel
from typing import Optional, List
from pprint import pprint
from langgraph.prebuilt import tools_condition
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
import os 
import json
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd 


os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')


class ExtractionSchema(BaseModel):
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    facebook: Optional[str] = None
    submission_form: Optional[str] = None
    fallback_submission_form: Optional[str] = None

    other_links: Optional[List[str]] = []
    needs_scraping: Optional[List[str]] = []

def initial_search(state: CuratorState) -> CuratorState:
    curator_name = state['curator_name']
    content = google_search.invoke({"query": f'{curator_name} music playlists'})
    filtered_results = filter_search_results.invoke({'items': content, 'entity_name': curator_name})
    state['messages'] = filtered_results

    return state

def LLM_extraction(state: CuratorState) -> CuratorState:
    llm = ChatGroq(model='llama-3.3-70b-versatile')
    # llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')
    structured_llm = llm.with_structured_output(ExtractionSchema)
    curator_name =  state['curator_name']

    PROMPT = AGENT_PROMPT.format(
        curator_name=curator_name,
        current_state=json.dumps({
            'instagram': state.get('instagram'),
            'twitter': state.get('twitter'),
            'facebook': state.get('facebook'),
            'submission_form': state.get('submission_form'),
            'other_links': state.get('other_links', []),
            'needs_scraping': state.get('needs_scraping', []),
            'spotify_url': state.get('spotify_url')
        }, indent=2)
    )

    messages = [
        ("system", PROMPT),
        ("human", f'{state["messages"]}')
    ]
    if state['messages']:
        result = structured_llm.invoke(messages)
   
        state['messages'] = [] 

        if result.instagram and not state["instagram"]:
            state["instagram"] = result.instagram

        if result.twitter:
            state["twitter"] = result.twitter

        if result.facebook:
            state["facebook"] = result.facebook

        if result.submission_form:
            state["submission_form"] = result.submission_form

        if result.other_links and not state['any_other_handle']:
            state["any_other_handle"] = result.other_links

        if result.needs_scraping:
            arr = [r for r in result.needs_scraping if r not in state['scraped_urls']]
            state["needs_scraping"] = arr

        missing = []
        for handle in ['instagram', 'twitter', 'facebook', 'submission_form']:
            if not state[handle] and (handle not in state['searched_handles']):
                missing.append(handle)
        state["missing"] = missing

    pprint(state)
    print("\n")
    return state


def scrape(state: CuratorState) -> CuratorState:
    if not state['needs_scraping'] or state['scrape_count'] > 0:
        state['needs_scraping'] = []
        return state
    
    cur_url = state['needs_scraping'][-1]
    content = scrape_page.invoke({'url': cur_url})
    state['messages'] = [str(content)]
    state['scrape_count'] += 1

    state['scraped_urls'].append(state['needs_scraping'].pop())

    return state

def search(state: CuratorState) -> CuratorState:
    if not state['missing'] or state['search_count'] > 3:
        state['missing'] = []
        return state

    missing_handle = state['missing'][-1]
    curator_name = state['curator_name']

    if missing_handle in ['instagram', 'twitter', 'facebook']:
        query = f'site:{missing_handle}.com "{curator_name}"'
    else:
        query = curator_name + ' Music ' + missing_handle
    content = google_search.invoke({'query': query})
    filtered_results = filter_search_results.invoke({'items': content, 'entity_name': curator_name})

    state['messages'] = filtered_results
    state['search_count'] += 1

    state['searched_handles'].append(state['missing'].pop())

    return state

def router(state: CuratorState) -> str:
    if not state['missing'] and not state['needs_scraping']:
        return 'END'
    if state['needs_scraping'] and state['scrape_count'] < 1:
        return 'scrape'
    if state['missing'] and state['search_count'] < 3:
        return 'search'
    return 'END'

graph = StateGraph(CuratorState)
# Nodes
graph.add_node("Initial_Search", initial_search)
graph.add_node("LLM_extraction", LLM_extraction)
graph.add_node("Scrape", scrape)
graph.add_node("Search", search)

# Edges
graph.add_edge(START, "Initial_Search")
graph.add_edge("Initial_Search", "LLM_extraction")
graph.add_conditional_edges("LLM_extraction", router, {"scrape": "Scrape", "search": "Search", "END": END})
graph.add_edge("Scrape", "LLM_extraction")
graph.add_edge("Search", "LLM_extraction")

workflow = graph.compile()

data = []
curators = [{'curator_name':'Filtr US','curator_spotify_url': 'https://open.spotify.com/user/filtr'},
            {'curator_name':'Indie Folk Central','curator_spotify_url': 'https://open.spotify.com/user/ykxuknpdqe4vrfi4lrn2gb76p'}]
for curator in curators:
    initial_state = create_initial_state(curator_name=curator['curator_name'], 
                                         curator_spotify_url=curator['curator_spotify_url'])
    
    final_state = workflow.invoke(initial_state)
    data.append({
        'curator_name': final_state['curator_name'],
        'spotify_url': final_state['spotify_url'],
        'instagram': final_state['instagram'],
        'twitter': final_state['twitter'],
        'facebook': final_state['facebook'],
        'submission_form': final_state['submission_form'],
        'any_other_handle': final_state['any_other_handle']
    })

df = pd.DataFrame(data)
df.to_csv('data/curator_metadata.csv', index=False)

pprint(data)






