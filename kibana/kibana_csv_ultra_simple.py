"""
Kibana CSV Download - Ultra Simple Version
Minimal waits, maximum compatibility
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

def download_kibana_csv():
    Path("downloads").mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        print("🚀 Starting...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate
        print("📊 Loading dashboard...")
        page.goto("https://demo.elastic.co/app/dashboards#/view/kubernetes-ff1b3850-bcb1-11ec-b64f-7dd6e8e82013?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-15m,to:now))")
        
        # Accept cookies
        try:
            page.click('button:has-text("Accept")', timeout=3000)
            print("✅ Cookies accepted")
        except:
            print("⏩ No cookie dialog")
        
        # Wait for load - intentionally long to ensure dashboard renders
        print("⏳ Waiting for page load (15s)...")
        time.sleep(15)
        
        # Scroll to bottom to find "Services"
        print("📜 Scrolling to bottom...")
        for _ in range(5):
            page.keyboard.press("PageDown")
            time.sleep(0.5)
        
        # Click "Services" link
        try:
            print("🔍 Looking for 'Services' link...")
            # Try specific text first, then broader search
            # User described: "[Metrics Kubernetes] Services"
            services_link = page.locator('a:has-text("[Metrics Kubernetes] Services"), button:has-text("[Metrics Kubernetes] Services")')
            
            # If specific selector fails, try just "Services" inside a header or link
            if not services_link.count():
                 services_link = page.locator(':text("Services")').last
            
            services_link.wait_for(state="visible", timeout=5000)
            services_link.scroll_into_view_if_needed()
            services_link.click()
            print("✅ Clicked 'Services' link")
            
            # Wait for new dashboard to load
            print("⏳ Waiting for 'Services' dashboard (10s)...")
            time.sleep(10)
            
        except Exception as e:
            print(f"❌ Failed to find/click 'Services': {e}")
            page.screenshot(path="error_services.png")
            print("Screenshot saved: error_services.png")
            # Don't return, maybe we are already there?
        
        # Click Download CSV
        print("🔍 Finding 'Service Information' panel...")
        try:
            # User feedback: 3-dots are on top right of "Service Information [Metrics Kubernetes]" table
            # Strategy: Find the panel by title, hover to reveal menu, then click.
            
            # 1. Find the panel title - focusing on "Service Information"
            # It might be in an h2, h3, or just a span with specific class
            # We use a broad text locator for the header
            panel_title = page.locator('h1, h2, h3, h4, h5, span').filter(has_text="Service Information").last
            
            if panel_title.count() == 0:
                 # Fallback: look for "[Metrics Kubernetes]" if "Service Information" fails
                 panel_title = page.locator('h1, h2, h3, h4, h5, span').filter(has_text="[Metrics Kubernetes]").last

            if panel_title.count() > 0:
                print("   Found panel title, hovering to reveal menu...")
                try:
                    panel_title.hover(force=True, timeout=2000)
                except:
                    print("   Could not hover over title, proceeding...")
                
                time.sleep(1)
                
                # 2. Look for the menu button specifically near this title
                # The button is usually a sibling or cousin in the DOM.
                # Locating by test-subj is best.
                
                # We need to find the button that is visibly close to this title.
                # In Playwright we can search for the button inside the same 'embeddable' container.
                # Finding the closest container: 
                # This is tricky without seeing DOM. 
                # Alternative: Use "right-of" or "near" layout selectors if finding container is hard?
                # or just find all menu buttons and pick the one that is visible?
                
                # Let's try to find the button using the panel title as a specialized scope
                # "Find a button with title 'Panel options' that is inside a container that also has 'Service Information'"
                
                # Locate the common parent (likely .embeddable)
                # We will try to find the button directly first
                menu_btn = page.locator('[data-test-subj="embeddablePanelToggleMenuIcon"]').first
                
                # If specifically finding the ONE for this panel is hard blindly, 
                # we can assume it's the *only* or *main* one visible in this view? 
                # No, there might be multiple.
                
                # Let's try locating the button by text proximity if possible, or just click the first visible one
                # if the specific one fails.
                
                if not menu_btn.is_visible():
                     menu_btn = page.locator('button[aria-label*="Panel options"]').first
                
                if menu_btn.is_visible():
                    print("   Clicking panel options button...")
                    menu_btn.click()
                    time.sleep(1)
                    
                    # 3. Choose "Download CSV"
                    # Try "Inspect" -> "Download CSV" flow as it's often the default for tables
                    print("   Checking for 'Inspect' or 'Download CSV'...")
                    
                    # Check for direct download first
                    download_item = page.locator('button:has-text("Download CSV"), span:has-text("Download CSV")')
                    
                    if not download_item.is_visible():
                        inspect_item = page.locator('button:has-text("Inspect"), span:has-text("Inspect")')
                        if inspect_item.is_visible():
                            print("   Opening Inspector...")
                            inspect_item.click()
                            time.sleep(3)
                            download_item = page.locator('button:has-text("Download CSV"), span:has-text("Download CSV"), [data-test-subj="inspectorDownloadCSV"]')
                    
                    if download_item.is_visible():
                         print("   Clicking 'Download CSV'...")
                         with page.expect_download(timeout=30000) as download_info:
                            download_item.first.click()
                         
                         download = download_info.value
                         filepath = Path("downloads") / download.suggested_filename
                         download.save_as(filepath)
                         
                         print(f"✅ SUCCESS! Downloaded to: {filepath}")
                         print(f"📊 File size: {filepath.stat().st_size} bytes")
                         
                         # Show preview
                         if filepath.exists():
                             try:
                                 with open(filepath, 'r', encoding='utf-8') as f:
                                     print("\n📝 First 3 lines:")
                                     for i, line in enumerate(f.readlines()[:3], 1):
                                         print(f"  {i}: {line.strip()[:80]}")
                             except Exception as read_err:
                                  print(f"⚠️ Could not read file preview: {read_err}")
                    else:
                        print("❌ 'Download CSV' option not found.")
                        page.screenshot(path="error_menu_items.png")
                else:
                    print("❌ Panel menu button not visible even after hover.")
                    page.screenshot(path="error_button_hidden.png")
            else:
                print("❌ Could not find panel with text 'Service Information'")
                page.screenshot(path="error_no_panel_title.png")

        except Exception as e:
            print(f"❌ Error downloading CSV: {e}")
            page.screenshot(path="error_download.png")
            print("Screenshot saved: error_download.png")
        
        print("\n✅ Done!")
        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    download_kibana_csv()
