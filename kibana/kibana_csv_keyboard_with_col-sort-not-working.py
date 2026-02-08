"""
Kibana CSV Download - Approach 2: Keyboard Shortcut (Improved v4)
Uses keyboard shortcuts to find the RIGHT hidden 3-dots menu.

Strategy:
1. Navigate to dashboard.
2. Scroll to "Service Information" panel.
3. Use TAB navigation to loop through ALL panel options buttons.
4. For each button found:
   - Open menu (Enter)
   - Check if "Download CSV" is inside (handling strict mode)
   - If not, Close menu (Escape) and CONTINUE Searching
5. Wait after download to ensure file is saved.
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

def download_csv_via_keyboard():
    """
    Use keyboard shortcuts to access the Inspector/Download CSV.
    """
    Path("downloads").mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        print("🚀 Kibana CSV Download - Keyboard Shortcut Shortcut (Improved v4)")
        print("=" * 60)
        
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to the Services dashboard
        url = "https://demo.elastic.co/app/dashboards#/view/kubernetes-ff1b3850-bcb1-11ec-b64f-7dd6e8e82013?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-15m,to:now))"
        print(f"📊 Loading: {url}")
        page.goto(url)
        
        # Accept cookies
        try:
            page.click('button:has-text("Accept")', timeout=3000)
            print("✅ Cookies accepted")
        except:
            print("⏩ No cookie dialog")
        
        # Wait for dashboard to load
        print("⏳ Waiting for dashboard (15s)...")
        time.sleep(15)
        
        # Scroll to bottom and click Services link
        print("📜 Scrolling to find 'Services' link...")
        for _ in range(5):
            page.keyboard.press("PageDown")
            time.sleep(0.5)
        
        try:
            services_link = page.locator('a:has-text("[Metrics Kubernetes] Services"), button:has-text("[Metrics Kubernetes] Services"), :text("[Metrics Kubernetes] Services")').first
            services_link.scroll_into_view_if_needed()
            services_link.click()
            print("✅ Clicked 'Services' link")
            
            # Wait for dashboard update
            print("⏳ Waiting for dashboard to update (10s)...")
            time.sleep(10)
            
        except Exception as e:
            print(f"⚠️ Could not click Services link: {e}")
        
        # --- Sorting Logic ---
        sort_column = "Created"  # Default sort column
        sort_order = "descending" # Default sort order
        
        # --- Sorting Logic ---
        sort_column = "Created"
        sort_order = "descending"
        
        # --- Sorting Logic ---
        sort_column = "Created"
        
        print(f"\n🔽 Attempting to sort by '{sort_column}' (descending) via column menu...")
        
        try:
            # 1. Locate the specific panel "Services Informations [Metrics Kubernetes]"
            # Use a robust text locator for the panel title
            panel_title = page.locator('h1, h2, h3, h4, span, div').filter(has_text="Services Informations [Metrics Kubernetes]").first
            
            if panel_title.count() > 0:
                print("   Found panel title 'Services Informations [Metrics Kubernetes]'")
                panel_title.scroll_into_view_if_needed()
                
                # The table should be within the same container or nearby.
                # We'll look for the table header "Created" globally first, but maybe we can scope it?
                # Actually, filtering for the specific header "Created" inside a table context is safest.
                
                # Find the TH containing "Created"
                # In Kibana EUI, the 3-dots button is often inside the TH.
                header_cell = page.locator("th").filter(has_text=sort_column).first
                
                if header_cell.count() > 0 and header_cell.is_visible():
                    print(f"   Found '{sort_column}' header cell.")
                    header_cell.scroll_into_view_if_needed()
                    header_cell.hover() # Hover might reveal the button
                    
                    # Look for the 3-dots button inside this header
                    # It often has an aria-label like "Column actions" or "Sorted by..." or just a class with "eui...".
                    # We'll try to find a button inside.
                    menu_button = header_cell.locator("button").last # Usually the last button is the menu (first might be sort toggle)
                    
                    if menu_button.count() > 0:
                        print("   Found menu button in header. Clicking...")
                        menu_button.click()
                        time.sleep(1) # Wait for menu to pop up
                        
                        # Look for "Sort descending" in the menu
                        sort_desc_option = page.locator('button, span, div').filter(has_text="Sort descending").first
                        
                        if sort_desc_option.count() > 0 and sort_desc_option.is_visible():
                            print("   Found 'Sort descending' option. Clicking...")
                            sort_desc_option.click()
                            time.sleep(2) # Wait for sort to apply
                            print("✅ Sorting triggered successfully.")
                        else:
                             print("⚠️ 'Sort descending' option not found in menu.")
                             # Maybe it's already sorted? check aria-checked?
                             # Or maybe the text is slightly different.
                             # Fallback: Print menu items
                             print("   (Menu items found: " + str(page.locator(".euiContextMenuItem").all_inner_texts()) + ")")
                             page.keyboard.press("Escape") # Close menu
                    else:
                        print("⚠️ Could not find menu button inside header cell.")
                else:
                    print(f"⚠️ Could not find visible '{sort_column}' table header.")
                    print("   🔍 Debugging: Dumping HTML of the panel's table area...")
                    try:
                        # Find the parent container of the title, then look for a table
                        # This is a bit rough, but let's try to get the table HTML
                        panel_container = panel_title.locator("xpath=../../..") # Go up a few levels
                        table = panel_container.locator("table")
                        if table.count() > 0:
                            print(f"   Table HTML (first 500 chars): {table.first.inner_html()[:500]}")
                        else:
                            print("   No <table> tag found nearby. Checking for div-based table...")
                            # Maybe it's divs
                            headers = panel_title.locator("xpath=../../..").locator('[role="columnheader"]')
                            print(f"   Found {headers.count()} div-based headers.")
                            for i in range(min(headers.count(), 5)):
                                print(f"   - Header {i}: {headers.nth(i).inner_text()}")
                    except Exception as ex:
                        print(f"   (Error dumping debug info: {ex})")
            else:
                 print("⚠️ Could not find panel 'Services Informations [Metrics Kubernetes]'.")
        
        except Exception as e:
            print(f"⚠️ Error during sorting: {e}")
        # ---------------------
            
        # ---------------------
        # ---------------------
            
        # Now try keyboard shortcuts to access Inspector
        print("\n🎹 Trying keyboard shortcuts to reach panel menu...")
        
        # Strategy: Focus specifically on the "Service Information" panel container first
        print("   Step 1: Clicking 'Service Information' panel to focus it...")
        try:
             # Find panel by text and get its parent container
             panel_header = page.locator('span:has-text("Service Information"), h3:has-text("Service Information")').first
             
             # CLicking the header sets accessibility focus roughly in the right area
             if panel_header.count() > 0:
                 panel_header.scroll_into_view_if_needed()
                 panel_header.click()
                 time.sleep(1)
             else:
                 print("   ⚠️ Heading 'Service Information' not found, clicking page body center...")
                 page.click("body")
        except:
             pass

        print("⚠️ Starting TAB navigation loop to find relevant panel menu...")
        
        # Strategy 3: Tab navigation loop to find the "Panel options" button
        # We start from the panel header focus (which we likely missed or is far up)
        # We need to cycle through tab stops until we find a "Panel options" button
        # AND verify it's the right one by checking its menu items.
        
        max_total_tabs = 150
        found_final_csv = False
        
        for i in range(max_total_tabs): 
            page.keyboard.press("Tab")
            time.sleep(0.05) # Fast tabs
            
            # Get info about focused element
            focused_meta = page.evaluate("""() => {
                const el = document.activeElement;
                return {
                    label: el.getAttribute('aria-label') || '',
                    test_subj: el.getAttribute('data-test-subj') || '',
                    text: el.innerText || ''
                }
            }""")
            
            focused_label = focused_meta['label'].lower()
            focused_test_subj = focused_meta['test_subj']
            
            # Debug output to trace navigation occasionally
            if i % 10 == 0: print(f"   [Tab {i}] Focused: label='{focused_label}' test_subj='{focused_test_subj}'")

            # Check if we hit A panel options button
            if (("panel options" in focused_label) or 
                ("options for" in focused_label) or 
                ("embeddablePanelToggleMenuIcon" in focused_test_subj)):
                
                print(f"✅ FOUND A Panel Options button at Tab {i}!")
                print("   Pressing ENTER to open menu and check contents...")
                page.keyboard.press("Enter")
                time.sleep(1.5) # Wait for animation
                
                # Check if this menu has what we want
                # Loop allows us to try the next panel if this isn't the one
                
                # Check 1: Direct Download CSV
                download_option = page.locator('button:has-text("Download CSV"), span:has-text("Download CSV")')
                
                # FIX: Check count AND use .first to avoid strict mode error
                if download_option.count() > 0 and download_option.first.is_visible():
                    print("   🎉 Found visible 'Download CSV', clicking...")
                    with page.expect_download(timeout=30000) as download_info:
                        download_option.first.click()
                    download = download_info.value
                    filepath = Path("downloads") / download.suggested_filename
                    download.save_as(filepath)
                    print(f"✅ SUCCESS! Downloaded: {filepath}")
                    
                    # Wait to ensure filesystem flush
                    print("⏳ Waiting for file to save...")
                    time.sleep(5)
                    
                    found_final_csv = True
                    break
                
                # Check 2: Inspect -> Download
                inspect_option = page.locator('button:has-text("Inspect"), span:has-text("Inspect")')
                if inspect_option.count() > 0 and inspect_option.first.is_visible():
                     print("   Found 'Inspect', clicking to check for CSV...")
                     inspect_option.first.click()
                     time.sleep(3)
                     
                     download_btn = page.locator('button:has-text("Download CSV"), [data-test-subj="inspectorDownloadCSV"]')
                     if download_btn.count() > 0 and download_btn.first.is_visible():
                         print("   🎉 Found 'Download CSV' in Inspector!")
                         with page.expect_download() as dl_info:
                             download_btn.first.click()
                         dl = dl_info.value
                         fp = Path("downloads") / dl.suggested_filename
                         dl.save_as(fp)
                         print(f"✅ SUCCESS! Downloaded: {fp}")
                         
                         # Wait to ensure filesystem flush
                         print("⏳ Waiting for file to save...")
                         time.sleep(50)
                         
                         found_final_csv = True
                         break
                     else:
                         print("   ❌ Download CSV not found in Inspector. Closing Inspector...")
                         # Close inspector to resume navigation? 
                         # Usually inspector takes over context. Might need to close flyout.
                         # Try pressing Escape
                         page.keyboard.press("Escape")
                         time.sleep(1)
                else:
                    print("   ❌ Neither 'Download CSV' nor 'Inspect' found in this menu.")
                    # Close the menu to continue tabbing
                    print("   Closing menu (Pressing Escape) and continuing search...")
                    page.keyboard.press("Escape")
                    time.sleep(1)
                    
        if not found_final_csv:
            print("❌ Exhausted all TAB attempts. Could not find a panel with CSV download.")
            # page.screenshot(path="error_tab_nav_exhausted.png") # commented out
        
        print("\n✅ Done!")
        time.sleep(2)
        browser.close()


if __name__ == "__main__":
    download_csv_via_keyboard()
