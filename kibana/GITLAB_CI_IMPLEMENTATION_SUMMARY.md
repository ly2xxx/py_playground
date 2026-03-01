# 🚀 GitLab CI Implementation for Kibana CSV Export - Summary

## 📦 What Was Created

Three comprehensive guides to help you implement Kibana CSV exports in GitLab CI/CD:

### 1. `.gitlab-ci.yml` - Pipeline Template
**Location:** `C:\code\py_playground\kibana\.gitlab-ci.yml`

**What it does:**
- ✅ Runs Playwright scripts in Docker containers
- ✅ Handles authentication via stored cookies
- ✅ Downloads CSV files as pipeline artifacts
- ✅ Supports scheduled runs (cron-like)
- ✅ Includes retry logic and timeout protection
- ✅ Optional notification hooks (Slack, email)

**Key features:**
```yaml
stages:
  - setup      # Validate environment
  - export     # Run Playwright script
  - notify     # Send success/failure alerts
```

**How to use:**
1. Copy `.gitlab-ci.yml` to your GitLab repo root
2. Configure CI/CD variables (see below)
3. Push to GitLab
4. Set up schedule or run manually

---

### 2. `COOKIE_EXTRACTION_GUIDE.md` - SSO Authentication Guide
**Location:** `C:\code\py_playground\kibana\COOKIE_EXTRACTION_GUIDE.md`

**What it covers:**
- ✅ How to extract session cookies from browser DevTools
- ✅ Using browser extensions (EditThisCookie, Cookie-Editor)
- ✅ Playwright helper script to save cookies automatically
- ✅ How to store cookies securely in GitLab
- ✅ Cookie refresh strategies for long-term automation
- ✅ Troubleshooting cookie authentication issues

**Quick steps:**
1. Log in to Kibana manually
2. Open Chrome DevTools → Application → Cookies
3. Copy `sid` or session cookie value
4. Store in GitLab CI/CD variables as `KIBANA_SESSION_COOKIE`
5. Enable **Masked** flag for security

---

### 3. `PLAYWRIGHT_KEYBOARD_HEADLESS_RESEARCH.md` - Keyboard Navigation Research
**Location:** `C:\code\py_playground\kibana\PLAYWRIGHT_KEYBOARD_HEADLESS_RESEARCH.md`

**Key findings:**
- ✅ **NO additional libraries needed!**
- ✅ `page.keyboard.press("Tab")` works identically in headless mode
- ✅ Built-in Playwright keyboard API is sufficient
- ✅ Tab navigation, Enter, Escape all work out-of-the-box
- ✅ Just change `headless=False` to `headless=True`

**Keyboard API examples:**
```python
# All of these work in headless mode:
page.keyboard.press("Tab")
page.keyboard.press("Enter")
page.keyboard.press("Escape")
page.keyboard.press("PageDown")
page.keyboard.press("Control+A")
```

**Performance:**
- Headless mode is ~2x faster to launch
- Lower memory usage
- Perfect for CI/CD environments

---

## 🎯 Implementation Checklist

### Phase 1: Local Testing (Do This First)

- [ ] **Test your existing script in headless mode:**
  ```python
  # Change this line in your script:
  browser = p.chromium.launch(headless=True)  # ← Set to True
  ```

- [ ] **Extract authentication cookies:**
  - [ ] Log in to Kibana in Chrome
  - [ ] Open DevTools → Application → Cookies
  - [ ] Copy session cookie value
  - [ ] Test locally with extracted cookies

- [ ] **Create cookie injection script:**
  ```python
  import os
  cookies = [{
      "name": "sid",
      "value": os.getenv("KIBANA_SESSION_COOKIE"),
      "domain": ".your-kibana.com",
      "path": "/"
  }]
  context = browser.new_context()
  context.add_cookies(cookies)
  ```

- [ ] **Verify downloads work in headless:**
  - [ ] Run script headless locally
  - [ ] Check that CSV files are saved
  - [ ] Verify file content is correct

---

### Phase 2: GitLab Setup

- [ ] **Create GitLab repository (if needed):**
  - [ ] Initialize repo or use existing project
  - [ ] Add your Python scripts
  - [ ] Add `requirements.txt`:
    ```txt
    playwright==1.41.0
    python-dotenv==1.0.0
    ```

- [ ] **Copy `.gitlab-ci.yml`:**
  - [ ] Copy from `C:\code\py_playground\kibana\.gitlab-ci.yml`
  - [ ] Place in repo root
  - [ ] Customize variables (URLs, script names)

- [ ] **Configure CI/CD variables:**
  - [ ] Go to GitLab: Settings → CI/CD → Variables
  - [ ] Add `KIBANA_SESSION_COOKIE` (masked + protected)
  - [ ] Add `KIBANA_URL` (optional override)
  - [ ] Add notification webhooks if needed

- [ ] **Update script for CI environment:**
  ```python
  # Make sure script reads from environment:
  import os
  
  kibana_url = os.getenv('KIBANA_URL', 'https://default-kibana.com')
  cookie_value = os.getenv('KIBANA_SESSION_COOKIE')
  ```

---

### Phase 3: First Pipeline Run

- [ ] **Push code to GitLab:**
  ```bash
  git add .gitlab-ci.yml
  git add kibana_csv_keyboard.py
  git add requirements.txt
  git commit -m "Add Kibana CSV export pipeline"
  git push origin main
  ```

- [ ] **Run pipeline manually:**
  - [ ] Go to CI/CD → Pipelines
  - [ ] Click "Run pipeline"
  - [ ] Select branch: `main`
  - [ ] Click "Run pipeline"

- [ ] **Monitor pipeline:**
  - [ ] Watch job logs
  - [ ] Look for authentication success
  - [ ] Check if CSV download triggers
  - [ ] Verify artifacts are created

- [ ] **Download and verify artifacts:**
  - [ ] Click on job → Browse artifacts
  - [ ] Download CSV files
  - [ ] Open and verify data

---

### Phase 4: Scheduling & Automation

- [ ] **Set up scheduled pipeline:**
  - [ ] Go to CI/CD → Schedules
  - [ ] Click "New schedule"
  - [ ] Set description: "Daily Kibana CSV Export"
  - [ ] Set interval: e.g., `0 9 * * *` (9 AM daily)
  - [ ] Target branch: `main`
  - [ ] Activate schedule

- [ ] **Configure notifications (optional):**
  - [ ] Add Slack webhook URL to variables
  - [ ] Uncomment notification stages in `.gitlab-ci.yml`
  - [ ] Test notification on next run

- [ ] **Set up cookie refresh reminder:**
  - [ ] Add calendar reminder (weekly or monthly)
  - [ ] Or implement automated refresh script

---

### Phase 5: Monitoring & Maintenance

- [ ] **Monitor pipeline success rate:**
  - [ ] Check CI/CD → Pipelines regularly
  - [ ] Investigate failures immediately

- [ ] **Common failure reasons:**
  - [ ] Cookie expired → Re-extract and update
  - [ ] Kibana UI changed → Update selectors in script
  - [ ] Network timeout → Increase wait times
  - [ ] GitLab runner issues → Check runner status

- [ ] **Keep cookies fresh:**
  - [ ] Refresh cookies before expiration
  - [ ] Monitor for authentication failures

- [ ] **Update documentation:**
  - [ ] Document any script customizations
  - [ ] Note cookie refresh schedule
  - [ ] Record troubleshooting steps

---

## 🔧 Customization Examples

### Multiple Dashboards

If you need to export from multiple dashboards:

**Option 1: Parallel jobs**
```yaml
export_dashboard_1:
  extends: .export_template
  variables:
    DASHBOARD_URL: "https://kibana.com/dashboard1"

export_dashboard_2:
  extends: .export_template
  variables:
    DASHBOARD_URL: "https://kibana.com/dashboard2"
```

**Option 2: Loop in script**
```python
dashboards = [
    "dashboard-id-1",
    "dashboard-id-2",
    "dashboard-id-3"
]

for dashboard_id in dashboards:
    url = f"https://kibana.com/app/dashboards#/view/{dashboard_id}"
    download_csv(url)
```

---

### Multiple Environments (Prod/Staging)

```yaml
export_prod:
  stage: export
  variables:
    KIBANA_URL: "https://kibana.prod.company.com"
    KIBANA_SESSION_COOKIE: $PROD_SESSION_COOKIE
  only:
    - schedules

export_staging:
  stage: export
  variables:
    KIBANA_URL: "https://kibana.staging.company.com"
    KIBANA_SESSION_COOKIE: $STAGING_SESSION_COOKIE
  only:
    - schedules
```

---

### Email CSV as Attachment

Add a step to email the CSV:

```yaml
email_csv:
  stage: notify
  image: python:3.11-slim
  script:
    - pip install sendgrid
    - python send_email.py
  artifacts:
    paths:
      - downloads/*.csv
  when: on_success
```

```python
# send_email.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment
import base64

csv_file = "downloads/export.csv"

with open(csv_file, 'rb') as f:
    data = f.read()

encoded = base64.b64encode(data).decode()

message = Mail(
    from_email='noreply@company.com',
    to_emails='team@company.com',
    subject='Kibana CSV Export',
    html_content='<p>Attached is the latest CSV export.</p>'
)

attachment = Attachment()
attachment.file_content = encoded
attachment.file_name = 'kibana_export.csv'
attachment.file_type = 'text/csv'
message.attachment = attachment

sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
response = sg.send(message)
print(f"Email sent: {response.status_code}")
```

---

## 🐛 Troubleshooting Guide

### Pipeline fails: "Playwright not found"

**Solution:**
```yaml
script:
  - pip install playwright
  - playwright install chromium  # Add this line!
```

### Pipeline fails: "Download timeout"

**Solution:**
```python
# Increase timeout in script
with page.expect_download(timeout=120000) as download_info:  # 2 minutes
    download_button.click()
```

### Cookie doesn't work in CI

**Debug steps:**
1. Check cookie domain matches Kibana URL
2. Verify cookie hasn't expired
3. Test cookie locally first
4. Check for IP whitelisting requirements
5. Try extracting ALL cookies (not just one)

### CSV file is empty

**Possible causes:**
- Time range has no data
- Wrong panel selected
- Export triggered before data loaded

**Solutions:**
```python
# Wait longer before clicking export
time.sleep(5)

# Or wait for specific element
page.wait_for_selector('table tbody tr', timeout=10000)
```

---

## 📚 File Locations Summary

```
C:\code\py_playground\kibana\
├── .gitlab-ci.yml                              # GitLab pipeline config
├── COOKIE_EXTRACTION_GUIDE.md                  # How to get/store cookies
├── PLAYWRIGHT_KEYBOARD_HEADLESS_RESEARCH.md    # Keyboard navigation research
├── GITLAB_CI_IMPLEMENTATION_SUMMARY.md         # This file
├── kibana_csv_keyboard.py                      # Your existing script
└── requirements.txt                            # Python dependencies
```

---

## ✅ Success Criteria

You'll know it's working when:

1. ✅ Pipeline runs successfully in GitLab
2. ✅ Authentication succeeds (no login redirect)
3. ✅ CSV files appear in pipeline artifacts
4. ✅ CSV files contain expected data
5. ✅ Scheduled runs execute automatically
6. ✅ Notifications arrive on success/failure

---

## 🎉 Next Steps

1. **Today:**
   - [ ] Test headless mode locally
   - [ ] Extract cookies from browser

2. **This week:**
   - [ ] Set up GitLab repo
   - [ ] Run first successful pipeline
   - [ ] Configure schedule

3. **Ongoing:**
   - [ ] Monitor pipeline health
   - [ ] Refresh cookies as needed
   - [ ] Optimize script for reliability

---

## 📞 Support Resources

- **Playwright Docs:** https://playwright.dev/python/
- **GitLab CI Docs:** https://docs.gitlab.com/ee/ci/
- **Your existing scripts:** `C:\code\py_playground\kibana\`

**Questions? Check the three guides created:**
1. `.gitlab-ci.yml` - Pipeline configuration
2. `COOKIE_EXTRACTION_GUIDE.md` - Authentication setup
3. `PLAYWRIGHT_KEYBOARD_HEADLESS_RESEARCH.md` - Technical details

**Good luck! 🚀**
