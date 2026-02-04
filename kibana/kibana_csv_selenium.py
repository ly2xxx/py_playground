"""
Kibana Dashboard CSV Download - Selenium Version
Updated to match Playwright steps:
1. Go to Kubernetes dashboard
2. Scroll to Services link
3. Click Services
4. Find hidden menu on Service Information panel
5. Download CSV
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import time

def download_kibana_csv_selenium(download_dir="./downloads"):
    """
    Automate CSV download from Kibana using Selenium.
    """
    # Ensure download directory exists
    download_path = Path(download_dir).absolute()
    download_path.mkdir(exist_ok=True)
    
    # Configure Chrome options
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": str(download_path),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless")
    
    print("🚀 Launching Chrome...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 15) # Default wait
    
    try:
        # 1. Navigate to Kibana demo (Kubernetes dashboard)
        url = "https://demo.elastic.co/app/dashboards#/view/kubernetes-ff1b3850-bcb1-11ec-b64f-7dd6e8e82013?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-15m,to:now))"
        print(f"📊 Loading: {url}")
        driver.get(url)
        
        # 2. Accept cookies
        try:
            accept_wait = WebDriverWait(driver, 5)
            accept_btn = accept_wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
            )
            print("🍪 Accepting cookies...")
            accept_btn.click()
        except:
            print("ℹ️  No cookie dialog or already accepted")
        
        # 3. Wait for dashboard to load
        print("⏳ Waiting for dashboard (15s)...")
        time.sleep(15) 
        
        # 4. Scroll to bottom to find "Services"
        print("📜 Scrolling to bottom...")
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(5):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            
        # 5. Click "[Metrics Kubernetes] Services" link
        print("🔍 Looking for 'Services' link...")
        try:
            # Try specific text
            # We use a broad XPath to find the link. 
            # Note: "Services" might be in a span inside an 'a' tag.
            services_xpath = "//a[contains(text(), '[Metrics Kubernetes] Services')] | //button[contains(text(), '[Metrics Kubernetes] Services')] | //*[text()='[Metrics Kubernetes] Services']"
            
            services_link = wait.until(
                EC.presence_of_element_located((By.XPATH, services_xpath))
            )
            
            # Scroll it into view
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});", services_link)
            time.sleep(1) # Wait for scroll
            
            # Click it
            print("   Found link, clicking...")
            try:
                services_link.click()
            except:
                # Fallback to JS click if overlapped
                driver.execute_script("arguments[0].click();", services_link)
            
            print("✅ Clicked 'Services' link")
            
            # Wait for navigation/dashboard update
            # We expect "Service Information" to appear
            print("⏳ Waiting for 'Service Information' panel (20s)...")
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Service Information')]")))
            time.sleep(5) # stabilized wait
            
        except Exception as e:
            print(f"❌ Failed to find or click 'Services' link: {e}")
            driver.save_screenshot("error_link_click.png")
            raise e # Stop execution here, don't continue!


        # 6. Find 'Service Information' panel and hidden menu
        print("🔍 Finding 'Service Information' panel...")
        try:
            # Find the header element
            # We look for h1-h6 or span with text. 
            # Note: XPath text() match handles exact text, contains() handles partial.
            panel_title = driver.find_element(By.XPATH, "//*[contains(text(), 'Service Information')]")
            
            if panel_title:
                print("   Found panel title, hovering to reveal menu...")
                actions = ActionChains(driver)
                actions.move_to_element(panel_title).perform()
                time.sleep(2) # Wait for hover effect
                
                # Look for the menu button (3-dots)
                # It is usually having data-test-subj="embeddablePanelToggleMenuIcon"
                print("   Looking for menu button...")
                try:
                    # Try finding visible button first
                    menu_btn = driver.find_element(By.CSS_SELECTOR, '[data-test-subj="embeddablePanelToggleMenuIcon"]')
                    if not menu_btn.is_displayed():
                        # Try finding closer to title if possible, or just force find
                        # In Selenium finding "closest" is hard without complex XPath.
                        # We assume the hover made it visible.
                        pass
                except:
                    # Fallback locator
                    try:
                         menu_btn = driver.find_element(By.XPATH, "//button[@aria-label='Panel options']")
                    except:
                        menu_btn = None

                if menu_btn:
                    print("   Clicking panel options button...")
                    # Sometimes standard click fails if element is moving or obscured
                    try:
                        menu_btn.click()
                    except:
                         driver.execute_script("arguments[0].click();", menu_btn)
                    
                    time.sleep(1)
                    
                    # 7. Click Download CSV
                    print("   Checking menu options...")
                    # XPATH for Download CSV
                    download_xpath = "//button[contains(text(), 'Download CSV')] | //span[contains(text(), 'Download CSV')]"
                    
                    try:
                        download_btn = driver.find_element(By.XPATH, download_xpath)
                        if download_btn.is_displayed():
                            print("   Clicking 'Download CSV'...")
                            download_btn.click()
                        else:
                            raise Exception("Not visible")
                    except:
                        # Try "Inspect" -> "Download CSV"
                        print("   Checking 'Inspect'...")
                        inspect_xpath = "//button[contains(text(), 'Inspect')] | //span[contains(text(), 'Inspect')]"
                        inspect_btn = driver.find_element(By.XPATH, inspect_xpath)
                        inspect_btn.click()
                        time.sleep(3)
                        
                        print("   Inside Inspector, clicking 'Download CSV'...")
                        # Re-use download xpath or specific ID
                        download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, download_xpath)))
                        download_btn.click()
                    
                    # Wait for download
                    print("⏳ Waiting for download file...")
                    time.sleep(5)
                    
                    # Verify download
                    csv_files = list(download_path.glob("*.csv"))
                    if csv_files:
                        latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
                        print(f"✅ SUCCESS! Downloaded to: {latest_file}")
                        
                        # Preview content
                        try:
                            with open(latest_file, 'r', encoding='utf-8') as f:
                                print("\n📝 Preview:")
                                for i, line in enumerate(f.readlines()[:3], 1):
                                    print(f"  {i}: {line.strip()[:80]}")
                        except:
                            pass
                    else:
                        print("❌ No CSV found in downloads folder.")

                else:
                    print("❌ Panel menu button not found.")
                    driver.save_screenshot("error_selenium_no_menu.png")
            
        except Exception as e:
            print(f"❌ Error in panel interaction: {e}")
            driver.save_screenshot("error_selenium_panel.png")
            
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        driver.save_screenshot("error_selenium_critical.png")
    
    finally:
        print("\n✅ Done!")
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    download_kibana_csv_selenium()
