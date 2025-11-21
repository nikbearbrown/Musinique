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

def process_chunk(process_id, chunk_data, output_queue, batch_size=50):
    """
    Process a chunk of URLs in a separate process.
    Each process runs its own browser instance.
    Sends results in batches to avoid queue overflow.
    """
    print(f"[Process {process_id}] Starting with {len(chunk_data)} URLs")
    
    results = []
    
    with sync_playwright() as p:
        try:
            # Launch browser for this process
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-gpu',
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
                    
                    # Send batch to queue and clear results buffer
                    if len(results) >= batch_size:
                        output_queue.put((process_id, results.copy()))
                        print(f"[Process {process_id}] 📤 Sent batch of {len(results)} results to queue")
                        results = []
                    
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
                    
                    # Send batch if reached batch size
                    if len(results) >= batch_size:
                        output_queue.put((process_id, results.copy()))
                        print(f"[Process {process_id}] 📤 Sent batch of {len(results)} results to queue")
                        results = []
            
            browser.close()
            
        except Exception as e:
            print(f"[Process {process_id}] ✗ Error: {str(e)}")
            # Make sure to still return results for processed URLs even if error occurs
    
    # Send any remaining results
    if results:
        output_queue.put((process_id, results))
        print(f"[Process {process_id}] 📤 Sent final batch of {len(results)} results to queue")
    
    print(f"[Process {process_id}] ✓ Completed!")

def process_excel_file_parallel(input_file, output_file, num_processes=4, save_interval=100):
    """
    Process CSV file with multiple parallel processes.
    Saves results incrementally every save_interval rows.
    """
    print(f"{'='*70}")
    print(f"PARALLEL SPOTIFY URL VALIDATOR")
    print(f"{'='*70}")
    print(f"Reading file: {input_file}")
    print(f"Number of parallel processes: {num_processes}")
    print(f"Save interval: Every {save_interval} rows\n")
    
    # Read CSV
    df = pd.read_csv(input_file)
    total_rows = len(df)
    
    print(f"Total URLs to process: {total_rows}")
    print(f"{'='*70}\n")
    
    # Initialize result columns if they don't exist
    if 'is_playlist' not in df.columns:
        df['is_playlist'] = ""
    if 'is_profile' not in df.columns:
        df['is_profile'] = ""
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}\n")
    
    # Split data into chunks for each process
    chunk_size = (total_rows + num_processes - 1) // num_processes
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
    
    # Collect results continuously and save periodically
    all_results = {}
    results_since_last_save = 0
    total_collected = 0
    
    print(f"\n{'='*70}")
    print("Collecting and saving results...")
    print(f"{'='*70}\n")
    
    # Monitor queue while processes are running
    processes_finished = 0
    while processes_finished < len(processes):
        # Check if any process has finished
        for p in processes:
            if not p.is_alive() and p not in [proc for proc in processes if hasattr(proc, '_finished')]:
                processes_finished += 1
                setattr(p, '_finished', True)
        
        # Collect available results from queue
        while not output_queue.empty():
            try:
                process_id, results = output_queue.get(timeout=1)
                print(f"📥 Received {len(results)} results from Process {process_id}")
                
                for result in results:
                    all_results[result['row_idx']] = result
                    results_since_last_save += 1
                    total_collected += 1
                
                # Save if we've collected enough results
                if results_since_last_save >= save_interval:
                    print(f"\n💾 Saving checkpoint... ({total_collected} results collected so far)")
                    
                    # Update dataframe with all collected results
                    for row_idx, result in all_results.items():
                        df.loc[row_idx, 'is_playlist'] = result['is_playlist']
                        df.loc[row_idx, 'is_profile'] = result['is_profile']
                    
                    # Save to file
                    try:
                        df.to_csv(output_file, index=False, encoding='utf-8')
                        print(f"✅ Checkpoint saved! Total results: {total_collected}/{total_rows}")
                        results_since_last_save = 0
                    except Exception as e:
                        print(f"⚠️ Error saving checkpoint: {str(e)}")
                    
                    print(f"{'='*70}\n")
            
            except:
                break
        
        # Small sleep to prevent busy waiting
        time.sleep(0.5)
    
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    # Collect any remaining results
    print(f"\n{'='*70}")
    print("Collecting final results...")
    print(f"{'='*70}\n")
    
    while not output_queue.empty():
        try:
            process_id, results = output_queue.get(timeout=1)
            print(f"📥 Received {len(results)} final results from Process {process_id}")
            for result in results:
                all_results[result['row_idx']] = result
                total_collected += 1
        except:
            break
    
    print(f"\nTotal results collected: {total_collected}")
    
    # Final update and save
    print(f"\n{'='*70}")
    print(f"💾 Saving final results to: {output_file}")
    
    # Update dataframe with all results
    for row_idx, result in all_results.items():
        df.loc[row_idx, 'is_playlist'] = result['is_playlist']
        df.loc[row_idx, 'is_profile'] = result['is_profile']
    
    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✅ File saved successfully!")
        
        # Verify the file was created and has content
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"File size: {file_size:,} bytes")
            
            # Read back and verify
            verify_df = pd.read_csv(output_file)
            print(f"Verified rows in saved file: {len(verify_df)}")
            
            # Check how many rows have results
            playlist_results = verify_df['is_playlist'].notna() & (verify_df['is_playlist'] != '')
            profile_results = verify_df['is_profile'].notna() & (verify_df['is_profile'] != '')
            print(f"Rows with playlist results: {playlist_results.sum()}")
            print(f"Rows with profile results: {profile_results.sum()}")
        else:
            print(f"⚠️ Warning: Output file was not created!")
            
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")
        # Try saving to a backup location
        backup_file = "spotify_data_validated_backup.csv"
        print(f"Attempting to save to backup location: {backup_file}")
        df.to_csv(backup_file, index=False, encoding='utf-8')
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    # Print statistics
    print(f"{'='*70}")
    print(f"✅ COMPLETED!")
    print(f"{'='*70}")
    print(f"Total URLs processed: {total_rows}")
    print(f"Results collected: {len(all_results)}")
    print(f"Time taken: {duration}")
    print(f"Average time per URL: {duration.total_seconds() / total_rows:.2f}s")
    print(f"Output file: {output_file}")
    print(f"{'='*70}")

if __name__ == "__main__":
    INPUT_FILE = "spotify_data_complete.csv"
    OUTPUT_FILE = "processed/spotify_data_validated.csv"
    NUM_PROCESSES = 16  # Adjust based on your CPU cores
    SAVE_INTERVAL = 100  # Save after every 100 results collected
    
    # Set multiprocessing start method
    import multiprocessing
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        pass
    
    process_excel_file_parallel(INPUT_FILE, OUTPUT_FILE, NUM_PROCESSES, SAVE_INTERVAL)
