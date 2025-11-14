#!/usr/bin/env python3
"""
Domain Grabber - Complete Version (Fixed)
Non-parallel untuk reliability
"""

from playwright.sync_api import sync_playwright
import time
import os
import re
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

file_lock = threading.Lock()

def get_available_dates():
    """
    Ambil tanggal terbaru dan terlama yang tersedia
    """
    print("🔍 Detecting available dates...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.new_page()
        
        try:
            print("   → Checking newest dates...", end='', flush=True)
            page.goto("https://www.cubdomain.com/domains-registered-dates/1", timeout=30000)
            time.sleep(5)
            
            time_elements = page.locator('time[datetime]').all()
            
            if time_elements:
                first_time = time_elements[0].get_attribute('datetime')
                newest_date = first_time
                print(f" ✅")
            else:
                newest_date = None
                print(f" ❌")
            
            print("   → Checking oldest dates...", end='', flush=True)
            page.goto("https://www.cubdomain.com/domains-registered-dates/28", timeout=30000)
            time.sleep(10)
            
            try:
                page.wait_for_selector('time[datetime]', timeout=10000)
            except:
                pass
            
            time_elements = page.locator('time[datetime]').all()
            
            if time_elements:
                last_time = time_elements[-1].get_attribute('datetime')
                oldest_date = last_time
                print(f" ✅")
            else:
                oldest_date = "2017-06-30"
                print(f" ⚠️  (using fallback)")
            
            browser.close()
            
            return newest_date, oldest_date
            
        except Exception as e:
            browser.close()
            return None, None


def check_date_has_data(date):
    """
    Cek apakah tanggal ini punya data domain atau nggak
    """
    url = f"https://www.cubdomain.com/domains-registered-by-date/{date}/1"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        page_obj = context.new_page()
        
        try:
            page_obj.goto(url)
            time.sleep(5)
            
            # Cek ada domain atau nggak
            count = page_obj.locator('span.domain-name').count()
            
            browser.close()
            return count > 0
            
        except:
            browser.close()
            return False


def get_max_page(date):
    """
    Detect berapa total halaman untuk tanggal tertentu
    """
    url = f"https://www.cubdomain.com/domains-registered-by-date/{date}/1"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        page_obj = context.new_page()
        
        try:
            page_obj.goto(url, wait_until='domcontentloaded', timeout=30000)
            time.sleep(5)
            
            # Cek dulu ada domain atau nggak
            domain_count = page_obj.locator('span.domain-name').count()
            if domain_count == 0:
                browser.close()
                return 0
            
            last_page_links = page_obj.locator('a[title*="Page"][title*="of domains"]').all()
            
            if last_page_links:
                last_link = last_page_links[-1]
                last_page_text = last_link.inner_text().strip()
                max_page = int(last_page_text)
            else:
                max_page = 1
            
            browser.close()
            return max_page
            
        except:
            browser.close()
            return 0


def grab_page(date, page):
    """
    Grab domain dari 1 halaman (non-parallel, lebih reliable)
    """
    url = f"https://www.cubdomain.com/domains-registered-by-date/{date}/{page}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        page_obj = context.new_page()
        
        try:
            page_obj.goto(url)
            time.sleep(5)
            
            domains = page_obj.locator('span.domain-name').all_text_contents()
            
            browser.close()
            
            return [d.strip() for d in domains if d.strip()]
            
        except:
            browser.close()
            return []


def grab_page_parallel(date, page):
    """
    Grab domain dari 1 halaman (untuk parallel mode)
    """
    url = f"https://www.cubdomain.com/domains-registered-by-date/{date}/{page}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        page_obj = context.new_page()
        
        try:
            page_obj.goto(url)
            time.sleep(5)
            
            domains = page_obj.locator('span.domain-name').all_text_contents()
            
            browser.close()
            
            return page, [d.strip() for d in domains if d.strip()]
            
        except:
            browser.close()
            return page, []


def save_domains_threadsafe(domains, filename):
    """
    Save domains thread-safe
    """
    with file_lock:
        with open(filename, 'a', encoding='utf-8') as f:
            for domain in domains:
                f.write(f"{domain}\n")


def grab_single_date(date, start_page, end_page, output_file, use_parallel=False, workers=5):
    """
    Grab semua halaman untuk 1 tanggal
    """
    if use_parallel:
        # Parallel mode
        total_domains = 0
        pages_to_grab = list(range(start_page, end_page + 1))
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(grab_page_parallel, date, page): page for page in pages_to_grab}
            
            for future in as_completed(futures):
                page_num, domains = future.result()
                
                if domains:
                    save_domains_threadsafe(domains, output_file)
                    total_domains += len(domains)
                    print(f"      ✅ [{date}] Page {page_num}/{end_page} - {len(domains)} domains", flush=True)
                else:
                    print(f"      ⚠️  [{date}] Page {page_num}/{end_page} - 0 domains", flush=True)
        
        return total_domains
    else:
        # Sequential mode
        total_domains = 0
        
        for page in range(start_page, end_page + 1):
            print(f"      [{date}] Page {page}/{end_page}... ", end='', flush=True)
            
            domains = grab_page(date, page)
            
            if domains:
                with open(output_file, 'a', encoding='utf-8') as f:
                    for domain in domains:
                        f.write(f"{domain}\n")
                
                total_domains += len(domains)
                print(f"✅ {len(domains)} domains | Total: {total_domains}")
            else:
                print(f"⚠️  0 domains")
            
            if page < end_page:
                time.sleep(1)
        
        return total_domains


if __name__ == "__main__":
    # Welcome Screen
    print("\n" + "=" * 70)
    print("█▀▄ █▀█ █▀▄▀█ ▄▀█ █ █▄ █   █▀▀ █▀█ ▄▀█ █▄▄ █▄▄ █▀▀ █▀█")
    print("█▄▀ █▄█ █ ▀ █ █▀█ █ █ ▀█   █▄█ █▀▄ █▀█ █▄█ █▄█ ██▄ █▀▄")
    print("=" * 70)
    print("           CubDomain Mass Domain Grabber v1.0")
    print("=" * 70)
    print()
    print("  📦 Tool Features:")
    print("     • Auto detect available date ranges")
    print("     • Single date & date range grabbing")
    print("     • Parallel processing for speed")
    print("     • Auto skip empty dates")
    print("     • Custom output filename")
    print()
    print("  👤 Created by:")
    print("     GitHub: https://github.com/pengodehandal/")
    print()
    print("  ⚠️  Disclaimer:")
    print("     Use responsibly. Respect rate limits and ToS.")
    print("=" * 70)
    
    input("\nPress Enter to continue... ")
    print("\n" * 2)
    
    print("=" * 70)
    print("🔍 INITIALIZING DOMAIN GRABBER")
    print("=" * 70)
    print()
    
    newest, oldest = get_available_dates()
    
    print()
    if newest and oldest:
        print("✅ Date Range Detection Success")
        print(f"   📅 Newest: {newest}")
        print(f"   📅 Oldest: {oldest}")
    else:
        print("⚠️  Using default date range")
        newest = "2025-11-13"
        oldest = "2017-06-30"
    
    print()
    print("=" * 70)
    print("📋 SELECT MODE")
    print("=" * 70)
    print("  [1] Single Date Grabbing")
    print("      → Grab domains from one specific date")
    print()
    print("  [2] Date Range Grabbing")
    print("      → Grab domains from multiple dates")
    print("=" * 70)
    
    mode = input("\n→ Select mode [1/2]: ").strip()
    
    if mode == "1":
        # Mode single date
        print()
        date_input = input(f"Enter date (YYYY-MM-DD) / Masukkan tanggal [{newest}]: ").strip()
        DATE = date_input if date_input else newest
        
        print(f"\n🔍 Checking date {DATE}...")
        max_page = get_max_page(DATE)
        
        if max_page == 0:
            print(f"❌ Date {DATE} not available!")
            exit()
        
        print(f"✅ Total pages: {max_page}")
        
        grab_all = input(f"\nGrab all {max_page} pages? (y/n): ").strip().lower()
        
        if grab_all == 'y':
            START_PAGE = 1
            END_PAGE = max_page
        else:
            START_PAGE = int(input("Start page: ").strip() or "1")
            END_PAGE = int(input(f"End page (max {max_page}): ").strip() or "1")
        
        # Parallel mode option
        use_parallel = input("\nUse parallel mode (faster)? (y/n): ").strip().lower() == 'y'
        workers = 5
        
        if use_parallel:
            workers_input = input("Number of threads [5]: ").strip()
            workers = int(workers_input) if workers_input else 5
        
        # Custom filename
        filename_input = input(f"\nOutput filename [domains_{DATE}.txt]: ").strip()
        
        if filename_input:
            # Pastikan diakhiri .txt
            if not filename_input.endswith('.txt'):
                filename_input += '.txt'
            OUTPUT_FILE = filename_input
        else:
            OUTPUT_FILE = f"domains_{DATE}.txt"
        
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        
        print()
        print("=" * 70)
        print(f"🚀 GRABBING {DATE}")
        if use_parallel:
            print(f"⚡ Mode: PARALLEL ({workers} threads)")
        else:
            print(f"🐢 Mode: SEQUENTIAL")
        print("=" * 70)
        
        total = grab_single_date(DATE, START_PAGE, END_PAGE, OUTPUT_FILE, use_parallel, workers)
        
        print()
        print("=" * 70)
        print("✅ COMPLETE!")
        print(f"📊 Total domains: {total}")
        print(f"💾 Saved to: {OUTPUT_FILE}")
        print("=" * 70)
        
    elif mode == "2":
        # Mode date range
        print()
        print("📅 DATE RANGE MODE")
        print("=" * 70)
        
        start_date_input = input(f"Start date (YYYY-MM-DD) [{oldest}]: ").strip()
        START_DATE = start_date_input if start_date_input else oldest
        
        end_date_input = input(f"End date (YYYY-MM-DD) [{newest}]: ").strip()
        END_DATE = end_date_input if end_date_input else newest
        
        print(f"\n🔍 Date range: {START_DATE} to {END_DATE}")
        
        try:
            start = datetime.strptime(START_DATE, "%Y-%m-%d")
            end = datetime.strptime(END_DATE, "%Y-%m-%d")
            
            if start > end:
                print("❌ Start date must be before end date!")
                exit()
            
            dates_list = []
            current = start
            while current <= end:
                dates_list.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)
            
            print(f"📊 Total dates: {len(dates_list)} days")
            
            confirm = input(f"\nGrab domains from {len(dates_list)} dates? (y/n): ").strip().lower()
            
            if confirm != 'y':
                exit()
            
            grab_all_pages = input("\nGrab all pages for each date? (y/n): ").strip().lower()
            
            # Parallel mode option
            use_parallel = input("Use parallel mode (faster)? (y/n): ").strip().lower() == 'y'
            workers = 5
            
            if use_parallel:
                workers_input = input("Number of threads [5]: ").strip()
                workers = int(workers_input) if workers_input else 5
            
            # Custom filename
            filename_input = input(f"\nOutput filename [domains_{START_DATE}_to_{END_DATE}.txt]: ").strip()
            
            if filename_input:
                # Pastikan diakhiri .txt
                if not filename_input.endswith('.txt'):
                    filename_input += '.txt'
                OUTPUT_FILE = filename_input
            else:
                OUTPUT_FILE = f"domains_{START_DATE}_to_{END_DATE}.txt"
            
            if os.path.exists(OUTPUT_FILE):
                os.remove(OUTPUT_FILE)
            
            print()
            print("=" * 70)
            print("🚀 STARTING DATE RANGE GRAB")
            if use_parallel:
                print(f"⚡ Mode: PARALLEL ({workers} threads)")
            else:
                print(f"🐢 Mode: SEQUENTIAL")
            print("=" * 70)
            
            grand_total = 0
            successful_dates = 0
            skipped_dates = 0
            dates_with_data = []
            
            for idx, date in enumerate(dates_list, 1):
                print(f"\n[Date {idx}/{len(dates_list)}] 📅 {date}", end='', flush=True)
                
                max_page = get_max_page(date)
                
                if max_page == 0:
                    print(f" ⚠️  No data - SKIPPED")
                    skipped_dates += 1
                    continue
                
                print(f" ✅ {max_page} pages")
                dates_with_data.append(date)
                
                if grab_all_pages == 'y':
                    START_PAGE = 1
                    END_PAGE = max_page
                else:
                    START_PAGE = 1
                    END_PAGE = 1
                
                total = grab_single_date(date, START_PAGE, END_PAGE, OUTPUT_FILE, use_parallel, workers)
                
                if total > 0:
                    grand_total += total
                    successful_dates += 1
                
                print(f"   ✅ Complete: {total} domains")
            
            print()
            print("=" * 70)
            print("🎉 ALL DATES COMPLETE!")
            print("=" * 70)
            print(f"📊 Total domains grabbed     : {grand_total}")
            print(f"✅ Dates with data           : {successful_dates}/{len(dates_list)}")
            print(f"⚠️  Dates skipped (no data)  : {skipped_dates}/{len(dates_list)}")
            print(f"💾 Saved to                  : {OUTPUT_FILE}")
            
            if dates_with_data:
                print(f"\n📅 Dates grabbed:")
                for d in dates_with_data:
                    print(f"   - {d}")
            
            print("=" * 70)
            
        except ValueError:
            print("❌ Invalid date format!")
    
    else:
        print("\n❌ Invalid mode!")
