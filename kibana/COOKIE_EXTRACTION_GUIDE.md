# 🍪 Cookie Extraction Guide for Kibana SSO Authentication

This guide shows you how to extract authentication cookies from your browser to use in GitLab CI/CD pipelines for automated Kibana CSV exports.

---

## 📋 Table of Contents

1. [Why Extract Cookies?](#why-extract-cookies)
2. [Method 1: Chrome DevTools (Recommended)](#method-1-chrome-devtools-recommended)
3. [Method 2: Browser Extensions](#method-2-browser-extensions)
4. [Method 3: Playwright Helper Script](#method-3-playwright-helper-script)
5. [How to Store Cookies in GitLab](#how-to-store-cookies-in-gitlab)
6. [Cookie Refresh Strategy](#cookie-refresh-strategy)
7. [Troubleshooting](#troubleshooting)

---

## Why Extract Cookies?

When Kibana uses SSO (Single Sign-On) authentication:
- ❌ You can't just pass username/password to a script
- ❌ SSO flows involve redirects, tokens, and complex protocols
- ✅ **Solution:** Use authenticated session cookies from your browser

**How it works:**
1. Log in to Kibana manually via browser (SSO flow completes)
2. Browser receives session cookies
3. Extract those cookies
4. Inject them into Playwright script
5. Script accesses Kibana as if you're logged in

---

## Method 1: Chrome DevTools (Recommended)

### Step-by-Step:

1. **Log in to Kibana** in Chrome
   - Open `https://your-kibana.company.com`
   - Complete SSO login flow
   - Verify you can see dashboards

2. **Open DevTools**
   - Press `F12` or `Ctrl+Shift+I` (Windows/Linux)
   - Press `Cmd+Option+I` (Mac)

3. **Navigate to Application Tab**
   - Click **Application** tab in DevTools
   - If you don't see it, click the `>>` arrow and select it

4. **View Cookies**
   - In left sidebar: **Storage** > **Cookies**
   - Click on your Kibana domain (e.g., `https://your-kibana.company.com`)

5. **Identify Session Cookie**
   Look for cookies with names like:
   - `sid` (common for session ID)
   - `elasticsearch_session`
   - `kibana_session`
   - `auth_token`
   - Any cookie with "session", "auth", or "token" in the name

6. **Copy Cookie Value**
   - Click on the cookie row
   - Right-click > **Copy** > **Copy cookie value**
   - Or manually select and copy the **Value** field

7. **Note Additional Cookie Properties**
   Important fields to record:
   ```
   Name:     sid
   Value:    eyJhbGciOiJIUzI1NiIs... (long string)
   Domain:   .your-kibana.company.com
   Path:     /
   Expires:  (check if it expires soon!)
   HttpOnly: ✓
   Secure:   ✓
   SameSite: Lax
   ```

### Example Screenshot:

```
DevTools > Application > Cookies > https://kibana.company.com

Name                Value                                   Domain              Path    Expires
─────────────────────────────────────────────────────────────────────────────────────────────────
sid                 eyJhbGciOiJIUzI1NiIs...                .kibana.company.com  /       Session
_ga                 GA1.2.123456789.123                     .kibana.company.com  /       2 years
csrf_token          a3d8f9e2b1c...                          kibana.company.com   /       1 hour
```

**Copy the `sid` value!**

---

## Method 2: Browser Extensions

### Option A: EditThisCookie (Chrome)

1. **Install Extension**
   - Go to: https://chrome.google.com/webstore/detail/editthiscookie/
   - Click **Add to Chrome**

2. **Use Extension**
   - Log in to Kibana
   - Click the cookie icon in toolbar
   - Find session cookie
   - Click **Export** (JSON format)
   - Copy the entire JSON

### Option B: Cookie-Editor (Firefox/Chrome)

1. **Install Extension**
   - Chrome: https://chrome.google.com/webstore/detail/cookie-editor/
   - Firefox: https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/

2. **Use Extension**
   - Log in to Kibana
   - Click extension icon
   - Click **Export** > **JSON**
   - Copy JSON output

---

## Method 3: Playwright Helper Script

Use this script to save cookies from an authenticated browser session:

```python
# save_cookies.py
"""
Helper script to log in to Kibana and save authentication cookies.
Run this manually to extract cookies for CI/CD use.
"""

from playwright.sync_api import sync_playwright
import json
from pathlib import Path

def save_kibana_cookies():
    """
    Open Kibana, let user log in manually, then save cookies.
    """
    with sync_playwright() as p:
        print("🚀 Opening browser...")
        browser = p.chromium.launch(headless=False)  # Keep visible
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate to Kibana
        kibana_url = "https://your-kibana.company.com"
        print(f"📊 Navigating to: {kibana_url}")
        page.goto(kibana_url)
        
        print("\n" + "=" * 60)
        print("🔐 PLEASE LOG IN MANUALLY NOW")
        print("=" * 60)
        print("1. Complete SSO authentication in the browser window")
        print("2. Wait until you see the Kibana home page")
        print("3. Press ENTER in this terminal when done")
        print("=" * 60)
        
        input("\nPress ENTER after logging in... ")
        
        # Wait a bit to ensure all cookies are set
        page.wait_for_timeout(2000)
        
        # Extract cookies
        cookies = context.cookies()
        
        print("\n📋 Cookies extracted:")
        for cookie in cookies:
            print(f"   - {cookie['name']}: {cookie['value'][:30]}...")
        
        # Save to file
        output_file = Path("kibana_cookies.json")
        with open(output_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"\n✅ Cookies saved to: {output_file}")
        print(f"📊 Total cookies: {len(cookies)}")
        
        # Also save just the session cookie value for easy copy-paste
        session_cookies = [c for c in cookies if 'sid' in c['name'].lower() or 'session' in c['name'].lower()]
        
        if session_cookies:
            print("\n🎯 Likely session cookies:")
            for cookie in session_cookies:
                print(f"\n   Name:   {cookie['name']}")
                print(f"   Value:  {cookie['value']}")
                print(f"   Domain: {cookie['domain']}")
                print(f"   Expires: {cookie.get('expires', 'Session')}")
        
        browser.close()
        print("\n✅ Done! Use the cookie value in GitLab CI/CD variables.")

if __name__ == "__main__":
    save_kibana_cookies()
```

**Run it:**
```bash
python save_cookies.py
```

---

## How to Store Cookies in GitLab

### Step-by-Step:

1. **Go to GitLab Project**
   - Open your project in GitLab
   - Navigate to **Settings** > **CI/CD**

2. **Expand Variables Section**
   - Click **Variables** > **Expand**

3. **Add New Variable**
   - Click **Add variable**

4. **Configure Variable:**
   ```
   Type:        Variable
   Environment: All
   Key:         KIBANA_SESSION_COOKIE
   Value:       [paste the cookie value here]
   Protected:   ✓ (if running on protected branches)
   Masked:      ✓ (highly recommended to hide in logs)
   Expand:      ✗
   ```

5. **Click Add Variable**

### Multiple Cookies (if needed):

If you need multiple cookies, store them as JSON:

**Variable name:** `KIBANA_COOKIES`
**Value:**
```json
[
  {
    "name": "sid",
    "value": "eyJhbGciOiJIUzI1NiIs...",
    "domain": ".kibana.company.com",
    "path": "/",
    "httpOnly": true,
    "secure": true,
    "sameSite": "Lax"
  },
  {
    "name": "csrf_token",
    "value": "a3d8f9e2b1c...",
    "domain": "kibana.company.com",
    "path": "/",
    "httpOnly": false,
    "secure": true,
    "sameSite": "Strict"
  }
]
```

**In your script:**
```python
import os
import json

cookies_json = os.getenv('KIBANA_COOKIES')
cookies = json.loads(cookies_json)

context = browser.new_context()
context.add_cookies(cookies)
```

---

## Cookie Refresh Strategy

### Problem: Cookies Expire

Most session cookies expire after:
- **Session end** (browser closes)
- **Inactivity timeout** (30 min - 24 hours)
- **Absolute timeout** (7-30 days)

### Solutions:

#### Option 1: Manual Refresh (Simple)
- Re-extract cookies every week
- Update GitLab CI/CD variable
- Set calendar reminder

#### Option 2: Pre-Pipeline Refresh (Better)
Create a script that runs before the main pipeline:

```python
# refresh_cookies.py
"""
Automated cookie refresh script.
Logs in, extracts fresh cookies, updates GitLab variable via API.
"""

import os
import requests
from playwright.sync_api import sync_playwright

def refresh_and_update_cookies():
    # 1. Login and get fresh cookies (using saved credentials)
    cookies = login_and_get_cookies()
    
    # 2. Update GitLab CI/CD variable via API
    gitlab_token = os.getenv('GITLAB_API_TOKEN')
    project_id = os.getenv('CI_PROJECT_ID')
    
    response = requests.put(
        f'https://gitlab.company.com/api/v4/projects/{project_id}/variables/KIBANA_SESSION_COOKIE',
        headers={'PRIVATE-TOKEN': gitlab_token},
        json={'value': cookies['sid']}
    )
    
    if response.status_code == 200:
        print("✅ Cookie refreshed in GitLab!")
    else:
        print(f"❌ Failed to update: {response.text}")

def login_and_get_cookies():
    # Implement SSO login automation here
    # WARNING: This is complex and brittle
    pass
```

#### Option 3: Service Account / API Token (Best)
- Request a service account from IT/Security
- Use API token instead of cookies
- Tokens usually have longer lifetime or can be refreshed programmatically

**Check if your Kibana supports:**
- Elasticsearch API keys
- Kibana service tokens
- OAuth2 client credentials flow

---

## Troubleshooting

### Cookie doesn't work in CI pipeline

**Possible causes:**
1. **Cookie expired**
   - Check `Expires` timestamp
   - Re-extract fresh cookie

2. **Wrong domain**
   - Ensure `domain` matches your Kibana URL
   - Try with/without leading `.` (dot)
   - Example: `.kibana.company.com` vs `kibana.company.com`

3. **Missing cookies**
   - You might need multiple cookies
   - Extract ALL cookies from Kibana domain

4. **IP whitelist**
   - Your SSO might restrict by IP address
   - GitLab runners might be on different IPs
   - Contact IT to whitelist runner IPs

5. **User-Agent mismatch**
   - Some systems check User-Agent header
   - Add to Playwright:
   ```python
   context = browser.new_context(
       user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
   )
   ```

### How to test cookies locally

```python
# test_cookies.py
from playwright.sync_api import sync_playwright

cookies = [
    {
        "name": "sid",
        "value": "YOUR_COOKIE_VALUE_HERE",
        "domain": ".kibana.company.com",
        "path": "/"
    }
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.add_cookies(cookies)
    
    page = context.new_page()
    page.goto("https://your-kibana.company.com")
    
    # Wait to see if you're logged in
    page.wait_for_timeout(10000)
    
    # Check URL - if redirected to login, cookies didn't work
    print(f"Current URL: {page.url}")
    
    browser.close()
```

### Cookie is masked but I need to see it

**Problem:** GitLab masks variable values in logs for security

**Solution:** Only unmask temporarily for debugging:

```yaml
script:
  # DON'T DO THIS IN PRODUCTION! Only for debugging
  - echo "Cookie (first 20 chars): ${KIBANA_SESSION_COOKIE:0:20}..."
```

**Better:** Save cookies to file, then inspect file in artifacts:

```yaml
script:
  - echo "$KIBANA_SESSION_COOKIE" > cookie_debug.txt
artifacts:
  paths:
    - cookie_debug.txt
  expire_in: 1 hour
```

---

## Security Best Practices

1. **Never commit cookies to Git**
   - Add `*.json` containing cookies to `.gitignore`
   - Use GitLab CI/CD variables instead

2. **Use masked variables**
   - Always enable **Masked** for cookie values
   - Prevents accidental exposure in logs

3. **Limit cookie scope**
   - Only store cookies for the exact domain needed
   - Don't copy unrelated cookies

4. **Rotate regularly**
   - Refresh cookies at least monthly
   - Immediately refresh if someone leaves the team

5. **Use protected variables**
   - Enable **Protected** if only running on protected branches
   - Prevents exposure in feature branch pipelines

6. **Audit access**
   - Monitor who can view/edit CI/CD variables
   - Use GitLab audit logs

---

## Summary Checklist

- [ ] Log in to Kibana manually
- [ ] Open browser DevTools > Application > Cookies
- [ ] Identify session cookie (usually `sid` or `*_session`)
- [ ] Copy cookie value
- [ ] Note domain, path, and expiration
- [ ] Add to GitLab CI/CD variables
- [ ] Enable **Masked** flag
- [ ] Test locally with `test_cookies.py`
- [ ] Run GitLab pipeline to verify
- [ ] Set reminder to refresh cookies before expiry

---

**Questions?**
- Check Kibana documentation for authentication requirements
- Contact your IT/Security team about service accounts
- Test cookie lifetime by checking `Expires` field in DevTools

**Good luck! 🍪**
