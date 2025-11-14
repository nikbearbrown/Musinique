import pandas as pd
from playwright.sync_api import sync_playwright
import time
import re
import random
from multiprocessing import Process, Queue
import os
from datetime import datetime

def human_like_mouse_movement(page):
    """Simulate human-like mouse movements"""
    try:
        for _ in range(random.randint(1, 3)):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.1, 0.3))
    except:
        pass

def check_spotify_url(page, url):
    """
    Check if a Spotify URL is a valid playlist or profile link.
    Returns tuple: (is_playlist_status, is_profile_status)
    """
    is_playlist = ""
    is_profile = ""
    
    if not url or pd.isna(url) or url.strip() == "":
        return ("", "")
    
    url = url.strip()
    
    # Check URL format
    playlist_match = re.search(r'spotify\.com/playlist/([a-zA-Z0-9]+)', url)
    user_match = re.search(r'spotify\.com/user/([a-zA-Z0-9]+)', url)
    
    try:
        # Random delay before navigation
        time.sleep(random.uniform(1.5, 4.0))
        
        response = page.goto(url, timeout=25000, wait_until="domcontentloaded")
        
        # Wait for page to fully load
        time.sleep(random.uniform(5.0, 7.0))
        
        # Try to wait for either error message or valid content
        try:
            page.wait_for_selector('h1, button[data-testid="play-button"]', timeout=8000)
        except:
            pass
        
        # Random mouse movements
        human_like_mouse_movement(page)
        
        current_url = page.url
        
        # Get page text
        try:
            page_html = page.content()
            page_text = page.locator('body').inner_text().lower()
        except:
            page_text = ""
            page_html = ""
        
        # Check if redirected to home page
        if current_url == "https://open.spotify.com/" or current_url == "https://open.spotify.com":
            if playlist_match or "/playlist/" in url:
                is_playlist = "invalid playlist"
            elif user_match or "/user/" in url:
                is_profile = "invalid profile link"
            return (is_playlist, is_profile)
        
        # PRIMARY CHECK: Look for error messages
        error_found = False
        
        if "couldn't find that playlist" in page_text or "couldn't find that playlist" in page_html.lower():
            is_playlist = "invalid playlist"
            error_found = True
        
        if "couldn't find that page" in page_text or "couldn't find that page" in page_html.lower():
            is_profile = "invalid profile link"
            error_found = True
        
        if "search for something else" in page_text or "search for something else" in page_html.lower():
            if not error_found:
                if "/playlist/" in current_url or playlist_match:
                    is_playlist = "invalid playlist"
                elif "/user/" in current_url or user_match:
                    is_profile = "invalid profile link"
            error_found = True
        
        # Check H1 for error
        try:
            h1_text = page.locator('h1').first.inner_text().lower()
            if "couldn't find" in h1_text:
                if "playlist" in h1_text:
                    is_playlist = "invalid playlist"
                elif "page" in h1_text:
                    is_profile = "invalid profile link"
                error_found = True
        except:
            pass
        
        if error_found:
            return (is_playlist, is_profile)
        
        # Validate based on URL type
        if "/playlist/" in current_url:
            # Double-check for error text
            if "couldn't find" in page_text or "search for something else" in page_text:
                is_playlist = "invalid playlist"
                return (is_playlist, is_profile)
            
            valid_indicators = []
            
            # Check for track links
            try:
                track_title_selectors = [
                    'div[data-testid="tracklist-row"] a[href*="/track/"]',
                    'a[data-testid="internal-track-link"]',
                    '[role="row"] a[href*="/track/"]'
                ]
                
                track_links = 0
                for selector in track_title_selectors:
                    count = page.locator(selector).count()
                    if count > 0:
                        track_links = count
                        break
                
                if track_links > 3:
                    valid_indicators.append(f"{track_links} track links")
            except:
                pass
            
            # Check for add button
            try:
                add_button_selectors = [
                    'button[data-testid="add-button"]',
                    'button[aria-label*="Add"]'
                ]
                
                for selector in add_button_selectors:
                    if page.locator(selector).count() > 0:
                        valid_indicators.append("add button")
                        break
            except:
                pass
            
            # Check for save count
            try:
                if "save" in page_text and any(char.isdigit() for char in page_text):
                    valid_indicators.append("save count")
            except:
                pass
            
            # Check for description
            try:
                description_selectors = [
                    '[data-testid="playlist-description"]',
                    'div[data-testid="entity-description"]'
                ]
                
                for selector in description_selectors:
                    if page.locator(selector).count() > 0:
                        valid_indicators.append("description")
                        break
            except:
                pass
            
            # Check for duration
            if ("hr" in page_text or "min" in page_text) and "about" in page_text:
                valid_indicators.append("duration info")
            
            if len(valid_indicators) >= 2:
                is_playlist = "valid playlist"
            else:
                is_playlist = "invalid playlist"
        
        elif "/user/" in current_url:
            valid_indicators = []
            
            if "public playlists" in page_text:
                valid_indicators.append("public playlists section")
            
            if "followers" in page_text or "follower" in page_text:
                valid_indicators.append("follower count")
            
            try:
                follow_selectors = [
                    'button:has-text("Follow")',
                    'button[aria-label*="Follow"]'
                ]
                
                for selector in follow_selectors:
                    if page.locator(selector).count() > 0:
                        valid_indicators.append("follow button")
                        break
            except:
                pass
            
            if "profile" in page_text:
                valid_indicators.append("profile indicator")
            
            try:
                playlist_cards = page.locator('div[data-testid="playlist-card"]').count()
                if playlist_cards > 0:
                    valid_indicators.append(f"{playlist_cards} playlist cards")
            except:
                pass
            
            if len(valid_indicators) >= 2:
                is_profile = "valid profile link"
            else:
                is_profile = "invalid profile link"
        
        else:
            if playlist_match or "/playlist/" in url:
                is_playlist = "invalid playlist"
            elif user_match or "/user/" in url:
                is_profile = "invalid profile link"
    
    except Exception as e:
        if "/playlist/" in url or playlist_match:
            is_playlist = "invalid playlist"
        elif "/user/" in url or user_match:
            is_profile = "invalid profile link"
    
    return (is_playlist, is_profile)

def process_chunk(process_id, chunk_data, output_queue):
    """
    Process a chunk of URLs in a separate process.
    Each process runs its own browser instance.
    """
    print(f"[Process {process_id}] Starting with {len(chunk_data)} URLs")
    
    results = []
    
    with sync_playwright() as p:
        try:
            # Launch browser for this process
            browser = p.chromium.launch(
                headless=True,  # Headless mode - no browser window
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-gpu',  # Better for headless
                    '--disable-dev-tools',
                ]
            )
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York',
            )
            
            context.set_extra_http_headers({
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            })
            
            page = context.new_page()
            
            # Mask automation
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            # Process each URL in this chunk
            for idx, row_data in enumerate(chunk_data):
                row_idx, row = row_data
                spotify_url = row.get('spotify_url', '')
                
                if spotify_url and not pd.isna(spotify_url) and spotify_url.strip():
                    print(f"[Process {process_id}] [{idx + 1}/{len(chunk_data)}] Processing row {row_idx + 1}: {spotify_url[:50]}...")
                    
                    is_playlist, is_profile = check_spotify_url(page, spotify_url)
                    
                    # Store result with original row index
                    result = {
                        'row_idx': row_idx,
                        'is_playlist': is_playlist,
                        'is_profile': is_profile
                    }
                    results.append(result)
                    
                    status = "✅" if (is_playlist and "valid" in is_playlist) or (is_profile and "valid" in is_profile) else "❌"
                    print(f"[Process {process_id}] {status} Row {row_idx + 1}: playlist=[{is_playlist}] profile=[{is_profile}]")
                    
                    # Random delay
                    delay = random.uniform(2.0, 5.0)
                    time.sleep(delay)
                    
                    # Longer break every 10 URLs
                    if (idx + 1) % 10 == 0:
                        break_time = random.uniform(10.0, 20.0)
                        print(f"[Process {process_id}] ☕ Break: {break_time:.1f}s")
                        time.sleep(break_time)
                else:
                    # Empty URL
                    result = {
                        'row_idx': row_idx,
                        'is_playlist': '',
                        'is_profile': ''
                    }
                    results.append(result)
            
            browser.close()
            
        except Exception as e:
            print(f"[Process {process_id}] ✗ Error: {str(e)}")
    
    # Send results back through queue
    output_queue.put((process_id, results))
    print(f"[Process {process_id}] ✓ Completed! Processed {len(results)} URLs")

def process_excel_file_parallel(input_file, output_file, num_processes=4):
    """
    Process CSV file with multiple parallel processes.
    """
    print(f"{'='*70}")
    print(f"PARALLEL SPOTIFY URL VALIDATOR")
    print(f"{'='*70}")
    print(f"Reading file: {input_file}")
    print(f"Number of parallel processes: {num_processes}\n")
    
    # Read CSV
    df = pd.read_csv(input_file)
    total_rows = len(df)
    
    print(f"Total URLs to process: {total_rows}")
    print(f"{'='*70}\n")
    
    # Initialize result columns
    df['is_playlist'] = ""
    df['is_profile'] = ""
    
    # Split data into chunks for each process
    chunk_size = (total_rows + num_processes - 1) // num_processes  # Ceiling division
    chunks = []
    
    for i in range(num_processes):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_rows)
        
        if start_idx < total_rows:
            # Create chunk with row index and data
            chunk = [(idx, row) for idx, row in df.iloc[start_idx:end_idx].iterrows()]
            chunks.append(chunk)
            print(f"Process {i + 1}: Rows {start_idx + 1} to {end_idx} ({len(chunk)} URLs)")
    
    print(f"\n{'='*70}")
    print("Starting parallel processing...")
    print(f"{'='*70}\n")
    
    start_time = datetime.now()
    
    # Create queue for collecting results
    output_queue = Queue()
    
    # Create and start processes
    processes = []
    for i, chunk in enumerate(chunks):
        p = Process(target=process_chunk, args=(i + 1, chunk, output_queue))
        p.start()
        processes.append(p)
    
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    # Collect results from queue
    print(f"\n{'='*70}")
    print("Collecting results from all processes...")
    print(f"{'='*70}\n")
    
    all_results = {}
    while not output_queue.empty():
        process_id, results = output_queue.get()
        print(f"Received {len(results)} results from Process {process_id}")
        for result in results:
            all_results[result['row_idx']] = result
    
    # Update dataframe with results
    for row_idx, result in all_results.items():
        df.at[row_idx, 'is_playlist'] = result['is_playlist']
        df.at[row_idx, 'is_profile'] = result['is_profile']
    
    # Save results
    print(f"\n{'='*70}")
    print(f"💾 Saving results to: {output_file}")
    df.to_csv(output_file, index=False)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    # Print statistics
    print(f"{'='*70}")
    print(f"✅ COMPLETED!")
    print(f"{'='*70}")
    print(f"Total URLs processed: {total_rows}")
    print(f"Time taken: {duration}")
    print(f"Average time per URL: {duration.total_seconds() / total_rows:.2f}s")
    print(f"Output file: {output_file}")
    print(f"{'='*70}")

if __name__ == "__main__":
    INPUT_FILE = "spotify_data.csv"
    OUTPUT_FILE = "spotify_data_validated.csv"
    NUM_PROCESSES = 4  # Adjust based on your CPU cores
    
    # Important: On macOS, you may need to set this
    # to avoid issues with multiprocessing
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)
    
    process_excel_file_parallel(INPUT_FILE, OUTPUT_FILE, NUM_PROCESSES)
