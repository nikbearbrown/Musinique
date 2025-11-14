import pandas as pd
from playwright.sync_api import sync_playwright
import time
import re
import random

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

def random_scroll(page):
    """Simulate human-like scrolling behavior"""
    try:
        scroll_amount = random.randint(100, 500)
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(0.3, 0.8))
        if random.random() > 0.6:
            page.evaluate(f"window.scrollBy(0, -{random.randint(50, 150)})")
            time.sleep(random.uniform(0.2, 0.5))
    except:
        pass

def check_spotify_url(page, url):
    """
    Check if a Spotify URL is a valid playlist or profile link.
    Uses specific text detection based on Spotify's error pages.
    
    Key indicators:
    - Invalid pages show "Couldn't find that playlist" or "Couldn't find that page"
    - Invalid pages show "Search for something else?"
    - Valid playlists show track list and play button
    - Valid profiles show "Public Playlists" section and follower count
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
        
        print(f"    Navigating to URL...")
        response = page.goto(url, timeout=25000, wait_until="domcontentloaded")
        
        # Wait longer for content to load (invalid pages take longer)
        print(f"    Waiting for page to fully load...")
        time.sleep(random.uniform(5.0, 7.0))  # Increased wait time
        
        # Try to wait for either error message or valid content
        try:
            # Wait for either error or valid content to appear
            page.wait_for_selector('h1, button[data-testid="play-button"]', timeout=8000)
        except:
            pass
        
        # Random mouse movements
        human_like_mouse_movement(page)
        
        # Get current URL
        current_url = page.url
        print(f"    Final URL: {current_url}")
        
        # Get all page text for analysis
        try:
            page_html = page.content()
            page_text = page.locator('body').inner_text().lower()
        except:
            page_text = ""
            page_html = ""
        
        # Check if redirected to home page
        if current_url == "https://open.spotify.com/" or current_url == "https://open.spotify.com":
            print("    ✗ Redirected to home page - INVALID")
            if playlist_match or "/playlist/" in url:
                is_playlist = "invalid playlist"
            elif user_match or "/user/" in url:
                is_profile = "invalid profile link"
            return (is_playlist, is_profile)
        
        # PRIMARY CHECK: Look for the exact error messages from your screenshots
        # This MUST be checked first before looking for valid indicators
        error_found = False
        
        # Check for "Couldn't find that playlist" (exact match from screenshot 2)
        if "couldn't find that playlist" in page_text or "couldn't find that playlist" in page_html.lower():
            print("    ✗ Found 'Couldn't find that playlist' - INVALID")
            is_playlist = "invalid playlist"
            error_found = True
        
        # Check for "Couldn't find that page" (exact match from screenshot 4)
        if "couldn't find that page" in page_text or "couldn't find that page" in page_html.lower():
            print("    ✗ Found 'Couldn't find that page' - INVALID")
            is_profile = "invalid profile link"
            error_found = True
        
        # Check for "Search for something else?" (appears on all error pages)
        if "search for something else" in page_text or "search for something else" in page_html.lower():
            print("    ✗ Found 'Search for something else?' - INVALID")
            if not error_found:
                if "/playlist/" in current_url or playlist_match:
                    is_playlist = "invalid playlist"
                elif "/user/" in current_url or user_match:
                    is_profile = "invalid profile link"
            error_found = True
        
        # Additional check: Look for the exclamation icon that appears on error pages
        try:
            # The error icon is visible on invalid pages
            h1_text = page.locator('h1').first.inner_text().lower()
            if "couldn't find" in h1_text:
                print(f"    ✗ Found error in H1: '{h1_text}' - INVALID")
                if "playlist" in h1_text:
                    is_playlist = "invalid playlist"
                elif "page" in h1_text:
                    is_profile = "invalid profile link"
                error_found = True
        except:
            pass
        
        if error_found:
            return (is_playlist, is_profile)
        
        # If no error found, validate based on URL type
        if "/playlist/" in current_url:
            print("    Checking playlist validity...")
            
            # CRITICAL: Check one more time for error text before validating
            if "couldn't find" in page_text or "search for something else" in page_text:
                print("      ✗ INVALID - Found error text in page")
                is_playlist = "invalid playlist"
                return (is_playlist, is_profile)
            
            # Look for specific valid playlist indicators from screenshot 1
            valid_indicators = []
            
            # Check 1: Look for actual song/track titles (NOT just play button)
            try:
                # Look for track titles - these exist on valid playlists but not error pages
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
                
                if track_links > 3:  # Must have actual track links
                    valid_indicators.append(f"{track_links} track links")
                    print(f"      ✓ Found {track_links} track links")
            except:
                pass
            
            # Check 2: Look for the Add to playlist button (+ button) - only on valid playlists
            try:
                add_button_selectors = [
                    'button[data-testid="add-button"]',
                    'button[aria-label*="Add"]'
                ]
                
                for selector in add_button_selectors:
                    if page.locator(selector).count() > 0:
                        valid_indicators.append("add button")
                        print("      ✓ Found add-to-playlist button")
                        break
            except:
                pass
            
            # Check 3: Look for follower/like count (only on valid playlists)
            try:
                # Valid playlists show "2,395 saves" or similar
                if "save" in page_text and any(char.isdigit() for char in page_text):
                    valid_indicators.append("save count")
                    print("      ✓ Found save/like count")
            except:
                pass
            
            # Check 4: Look for playlist description area
            try:
                description_selectors = [
                    '[data-testid="playlist-description"]',
                    'div[data-testid="entity-description"]'
                ]
                
                for selector in description_selectors:
                    if page.locator(selector).count() > 0:
                        valid_indicators.append("description")
                        print("      ✓ Found playlist description area")
                        break
            except:
                pass
            
            # Check 5: Look for duration info ("about 2 hr 30 min")
            if ("hr" in page_text or "min" in page_text) and "about" in page_text:
                valid_indicators.append("duration info")
                print("      ✓ Found duration information")
            
            # Decision for playlists - need at least 2 strong indicators
            if len(valid_indicators) >= 2:
                print(f"      ✅ VALID playlist (found: {', '.join(valid_indicators)})")
                is_playlist = "valid playlist"
            else:
                print(f"      ✗ INVALID playlist (only found: {', '.join(valid_indicators) if valid_indicators else 'nothing'})")
                is_playlist = "invalid playlist"
        
        elif "/user/" in current_url:
            print("    Checking profile validity...")
            
            valid_indicators = []
            
            # Check 1: Look for "Public Playlists" text (from screenshot 3)
            if "public playlists" in page_text:
                valid_indicators.append("public playlists section")
                print("      ✓ Found 'Public Playlists' section")
            
            # Check 2: Look for follower count (e.g., "139,909 Followers" from screenshot 3)
            if "followers" in page_text or "follower" in page_text:
                valid_indicators.append("follower count")
                print("      ✓ Found follower information")
            
            # Check 3: Look for "Follow" button (appears on valid profiles)
            try:
                follow_selectors = [
                    'button:has-text("Follow")',
                    'button[aria-label*="Follow"]'
                ]
                
                for selector in follow_selectors:
                    if page.locator(selector).count() > 0:
                        valid_indicators.append("follow button")
                        print("      ✓ Found Follow button")
                        break
            except:
                pass
            
            # Check 4: Look for "Profile" badge/indicator
            if "profile" in page_text:
                valid_indicators.append("profile indicator")
                print("      ✓ Found profile indicator")
            
            # Check 5: Look for playlist cards/thumbnails
            try:
                playlist_cards = page.locator('div[data-testid="playlist-card"]').count()
                if playlist_cards > 0:
                    valid_indicators.append(f"{playlist_cards} playlist cards")
                    print(f"      ✓ Found {playlist_cards} playlist cards")
            except:
                pass
            
            # Decision for profiles
            if len(valid_indicators) >= 2:
                print(f"      ✅ VALID profile (found: {', '.join(valid_indicators)})")
                is_profile = "valid profile link"
            else:
                print(f"      ✗ INVALID profile (only found: {', '.join(valid_indicators) if valid_indicators else 'nothing'})")
                is_profile = "invalid profile link"
        
        else:
            # Fallback: determine based on original URL
            print("    Unknown page type, using URL pattern...")
            if playlist_match or "/playlist/" in url:
                is_playlist = "invalid playlist"
            elif user_match or "/user/" in url:
                is_profile = "invalid profile link"
    
    except Exception as e:
        print(f"    ✗ Exception occurred: {str(e)}")
        # Determine type based on URL structure
        if "/playlist/" in url or playlist_match:
            is_playlist = "invalid playlist"
        elif "/user/" in url or user_match:
            is_profile = "invalid profile link"
    
    return (is_playlist, is_profile)

def process_excel_file(input_file, output_file):
    """
    Process CSV file with Spotify URLs and add validation columns.
    """
    print(f"{'='*70}")
    print(f"SPOTIFY URL VALIDATOR")
    print(f"{'='*70}")
    print(f"Reading file: {input_file}\n")
    
    df = pd.read_csv(input_file)
    
    # Initialize new columns
    df['is_playlist'] = ""
    df['is_profile'] = ""
    
    print(f"Found {len(df)} rows to process\n")
    print(f"{'='*70}\n")
    
    with sync_playwright() as p:
        # Launch browser
        print("Launching browser...")
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
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
        
        print("Browser ready!\n")
        
        # Process each row
        for idx, row in df.iterrows():
            spotify_url = row.get('spotify_url', '')
            
            if spotify_url and not pd.isna(spotify_url) and spotify_url.strip():
                print(f"{'─'*70}")
                print(f"[{idx + 1}/{len(df)}] {spotify_url}")
                print(f"{'─'*70}")
                
                is_playlist, is_profile = check_spotify_url(page, spotify_url)
                
                df.at[idx, 'is_playlist'] = is_playlist
                df.at[idx, 'is_profile'] = is_profile
                
                result_icon = "✅" if (is_playlist and "valid" in is_playlist) or (is_profile and "valid" in is_profile) else "❌"
                print(f"\n{result_icon} RESULT: playlist=[{is_playlist}] | profile=[{is_profile}]")
                
                # Random delay
                delay = random.uniform(3.0, 8.0)
                print(f"⏳ Waiting {delay:.1f}s before next request...\n")
                time.sleep(delay)
                
                # Longer breaks
                if (idx + 1) % random.randint(5, 10) == 0:
                    break_time = random.uniform(15.0, 30.0)
                    print(f"{'='*70}")
                    print(f"☕ BREAK TIME: {break_time:.1f}s")
                    print(f"{'='*70}\n")
                    time.sleep(break_time)
            else:
                print(f"[{idx + 1}/{len(df)}] ⏭️  Skipping: No URL\n")
        
        print(f"\n{'='*70}")
        print("Closing browser...")
        browser.close()
    
    # Save results
    print(f"{'='*70}")
    print(f"💾 Saving results to: {output_file}")
    df.to_csv(output_file, index=False)
    print(f"✅ Done! Processed {len(df)} rows")
    print(f"{'='*70}")

if __name__ == "__main__":
    INPUT_FILE = "spotify_data.csv"
    OUTPUT_FILE = "spotify_data_validated.csv"
    
    process_excel_file(INPUT_FILE, OUTPUT_FILE)
