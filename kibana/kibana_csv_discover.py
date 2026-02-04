"""
Kibana CSV Download - Approach 3: Discover/Saved Search
Instead of exporting from a dashboard panel, navigate to Kibana's
Discover section where CSV export options are more accessible.

This approach:
1. Navigates to Discover
2. Selects the appropriate index pattern
3. Sets filters/query if needed
4. Uses the "Share" > "CSV Reports" option
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

def download_csv_via_discover():
    """
    Download CSV by navigating to Kibana Discover section.
    The export UI in Discover is typically more accessible than dashboard panels.
    """
    Path("downloads").mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        print("🚀 Kibana CSV Download - Discover/Saved Search Approach")
        print("=" * 60)
        
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate directly to Discover
        # For the demo site, we'll use their Discover page
        base_url = "https://demo.elastic.co"
        discover_url = f"{base_url}/app/discover"
        
        print(f"📊 Loading Discover: {discover_url}")
        page.goto(discover_url)
        
        # Accept cookies
        try:
            page.click('button:has-text("Accept")', timeout=3000)
            print("✅ Cookies accepted")
        except:
            print("⏩ No cookie dialog")
        
        # Wait for page to load
        print("⏳ Waiting for Discover to load (10s)...")
        time.sleep(10)
        
        # Check if we need to select a data view/index pattern
        print("🔍 Looking for data view selector...")
        
        # In modern Kibana, there's a data view selector
        data_view_selector = page.locator('[data-test-subj="dataViewSelectorButton"], [data-test-subj="indexPattern-switch-link"]')
        
        if data_view_selector.count() > 0:
            print("   Found data view selector, clicking...")
            data_view_selector.first.click()
            time.sleep(2)
            
            # Look for a kubernetes-related data view
            kube_option = page.locator(':text("kubernetes"), :text("metrics"), :text("metricbeat")')
            if kube_option.count() > 0:
                print("   Selecting kubernetes/metrics data view...")
                kube_option.first.click()
                time.sleep(3)
            else:
                # Just select the first available one
                first_option = page.locator('[data-test-subj="indexPattern-switch-link"]').first
                if first_option.count() > 0:
                    first_option.click()
                    time.sleep(3)
        
        # Set time range to get data
        print("📅 Setting time range...")
        time_picker = page.locator('[data-test-subj="superDatePickerToggleQuickMenuButton"], [data-test-subj="querySubmitButton"]')
        if time_picker.count() > 0:
            time_picker.first.click()
            time.sleep(1)
            
            # Select "Last 7 days" or similar
            last_7_days = page.locator(':text("Last 7 days")')
            if last_7_days.count() > 0:
                last_7_days.first.click()
                time.sleep(2)
        
        # Wait for data to load
        print("⏳ Waiting for data to load (5s)...")
        time.sleep(5)
        
        # Now try to share/export as CSV
        print("📤 Looking for Share/Export options...")
        
        # Method 1: Click "Share" button in top bar
        share_btn = page.locator('[data-test-subj="shareTopNavButton"], button:has-text("Share")')
        
        if share_btn.count() > 0 and share_btn.is_visible():
            print("   Found 'Share' button, clicking...")
            share_btn.first.click()
            time.sleep(2)
            
            # Look for CSV export option in the share menu
            csv_option = page.locator('[data-test-subj="sharePanel-CSVReports"], :text("CSV Reports"), :text("Generate CSV")')
            
            if csv_option.count() > 0 and csv_option.is_visible():
                print("   Found 'CSV Reports' option, clicking...")
                csv_option.first.click()
                time.sleep(2)
                
                # Look for generate/download button
                generate_btn = page.locator('[data-test-subj="generateReportButton"], button:has-text("Generate CSV"), button:has-text("Download")')
                
                if generate_btn.count() > 0:
                    print("   Clicking generate/download...")
                    with page.expect_download(timeout=60000) as download_info:
                        generate_btn.first.click()
                    
                    download = download_info.value
                    filepath = Path("downloads") / download.suggested_filename
                    download.save_as(filepath)
                    
                    print(f"✅ SUCCESS! Downloaded to: {filepath}")
                    print(f"📊 File size: {filepath.stat().st_size} bytes")
                else:
                    print("⚠️ Generate button not found.")
                    page.screenshot(path="error_discover_no_generate.png")
            else:
                print("⚠️ 'CSV Reports' option not in Share menu.")
                page.screenshot(path="error_discover_share_menu.png")
        else:
            print("⚠️ 'Share' button not found.")
            
            # Method 2: Try the table export directly
            print("   Trying alternative: Direct table export...")
            
            # Some Kibana versions have an export icon on the data table
            export_btn = page.locator('[data-test-subj="dataGridColumnSelectorButton"], [aria-label="Export"]')
            
            if export_btn.count() > 0:
                export_btn.first.click()
                time.sleep(1)
                
                csv_link = page.locator(':text("Export CSV")')
                if csv_link.count() > 0:
                    with page.expect_download(timeout=30000) as download_info:
                        csv_link.first.click()
                    
                    download = download_info.value
                    filepath = Path("downloads") / download.suggested_filename
                    download.save_as(filepath)
                    print(f"✅ Downloaded: {filepath}")
                else:
                    print("❌ CSV export option not found.")
                    page.screenshot(path="error_discover_export.png")
            else:
                print("❌ No export controls found in Discover.")
                page.screenshot(path="error_discover_no_export.png")
        
        print("\n✅ Done!")
        time.sleep(2)
        browser.close()


def download_csv_from_saved_search(saved_search_id=None):
    """
    Alternative: Load a saved search and export from there.
    Saved searches often have simpler export options.
    """
    Path("downloads").mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        print("\n" + "=" * 60)
        print("🔍 Saved Search Approach")
        print("=" * 60)
        
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # If we have a saved search ID, go directly to it
        if saved_search_id:
            url = f"https://demo.elastic.co/app/discover#/view/{saved_search_id}"
        else:
            # Go to saved objects and find saved searches
            url = "https://demo.elastic.co/app/management/kibana/objects"
        
        print(f"📊 Loading: {url}")
        page.goto(url)
        
        # Accept cookies
        try:
            page.click('button:has-text("Accept")', timeout=3000)
        except:
            pass
        
        time.sleep(5)
        
        # If we're on the management page, filter for saved searches
        if "objects" in url:
            print("📋 Looking for saved searches...")
            
            # Filter by type
            type_filter = page.locator('[data-test-subj="savedObjectsTableTypeFilter"]')
            if type_filter.count() > 0:
                type_filter.first.click()
                time.sleep(1)
                
                search_option = page.locator(':text("Search")')
                if search_option.count() > 0:
                    search_option.first.click()
                    time.sleep(2)
            
            # Click on the first saved search
            first_search = page.locator('a[data-test-subj="savedObjectsTableObjectLink"]').first
            if first_search.count() > 0:
                print("   Found a saved search, opening...")
                first_search.click()
                time.sleep(5)
                
                # Now we should be in Discover with the saved search loaded
                # Try to export from here
                share_btn = page.locator('[data-test-subj="shareTopNavButton"]')
                if share_btn.count() > 0:
                    share_btn.first.click()
                    time.sleep(2)
                    
                    csv_option = page.locator(':text("CSV Reports")')
                    if csv_option.count() > 0:
                        csv_option.first.click()
                        time.sleep(2)
                        
                        generate_btn = page.locator('button:has-text("Generate")')
                        if generate_btn.count() > 0:
                            with page.expect_download(timeout=60000) as download_info:
                                generate_btn.first.click()
                            
                            download = download_info.value
                            filepath = Path("downloads") / download.suggested_filename
                            download.save_as(filepath)
                            print(f"✅ Downloaded from saved search: {filepath}")
            else:
                print("❌ No saved searches found.")
        
        print("\n✅ Done!")
        time.sleep(2)
        browser.close()


if __name__ == "__main__":
    # Try the Discover approach first
    download_csv_via_discover()
    
    # Optionally try saved search approach
    # download_csv_from_saved_search()
