# Kibana Dashboard CSV Download Automation

Automated scripts to download CSV exports from Kibana dashboards programmatically.

## 📋 Overview

Two implementations provided:
1. **Playwright** - Modern, faster, better download handling
2. **Selenium** - Traditional, widely used, good browser compatibility

## 🎯 Demo Target

**URL:** `https://demo.elastic.co/app/dashboards#/view/edf84fe0-e1a0-11e7-b6d5-4dc382ef7f5b`

**Dashboard:** [Logs] Web Traffic  
**Panel:** "[Logs] Errors by host" data table

## 🚀 Quick Start

### Option 1: Playwright (Recommended)

```bash
# Install dependencies
pip install playwright
playwright install chromium

# Run script
python kibana_csv_download.py
```

### Option 2: Selenium

```bash
# Install dependencies
pip install selenium

# Make sure ChromeDriver is in PATH or install via:
# pip install webdriver-manager

# Run script
python kibana_csv_selenium.py
```

## 📁 Files

- `kibana_csv_download.py` - Playwright implementation
- `kibana_csv_selenium.py` - Selenium implementation
- `requirements_kibana.txt` - Python dependencies

## 🔍 How It Works

1. **Navigate** to Kibana demo dashboard
2. **Accept** cookie consent (if shown)
3. **Wait** for dashboard panels to load
4. **Scroll** to target data table panel
5. **Click** panel options menu (three-dot icon)
6. **Click** "Download CSV" button
7. **Capture** downloaded file
8. **Verify** file has data (not just headers)

## 📝 Key Features

- ✅ Automatic cookie handling
- ✅ Wait for dynamic content loading
- ✅ Download interception
- ✅ File verification (size check)
- ✅ Content preview
- ✅ Error handling with screenshots
- ✅ Configurable download directory

## 🛠️ Customization

### Change Download Directory

```python
download_kibana_csv(download_dir="./my_downloads")
```

### Headless Mode

**Playwright:**
```python
browser = p.chromium.launch(headless=True)
```

**Selenium:**
```python
chrome_options.add_argument("--headless")
```

### Different Dashboard

Update the URL in the script:
```python
url = "https://your-kibana-instance.com/app/dashboards#/view/YOUR_DASHBOARD_ID"
```

### Different Panel

Modify the button locator:
```python
panel_button = page.locator('button:has-text("Panel options for YOUR_PANEL_NAME")')
```

## 🐛 Troubleshooting

### "Panel options button not found"

- Dashboard might still be loading - increase wait time
- Panel name might be different - check the actual panel title
- Use `page.screenshot()` to debug

### "Download not captured"

- Check if CSV export is available for that panel type
- Verify download permissions in browser
- Check download directory permissions

### "File is empty (headers only)"

This is the issue mentioned in the Elastic discussion:
- Time range might be set to "Today" with no data
- Change time picker to a range with data (e.g., "Last 7 days")
- Automate time range selection before download

## 📚 Next Steps

### Automate Time Range Selection

```python
# Click time picker
time_picker = page.locator('button:has-text("Last 7 days")')
time_picker.click()

# Select different range
page.locator('button:has-text("Last 30 days")').click()
```

### Handle Multiple Panels

```python
panels = ["[Logs] Errors by host", "[Logs] Response Codes", "Other Panel"]
for panel_name in panels:
    download_panel_csv(panel_name)
```

### Schedule with Cron

```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/scripts && python kibana_csv_download.py
```

## 🔗 References

- **Elastic Discussion:** https://discuss.elastic.co/t/download-csv-from-dashboard-panel
- **Playwright Docs:** https://playwright.dev/python/
- **Selenium Docs:** https://selenium-python.readthedocs.io/

## ⚖️ License

MIT License - Free to use and modify

## 🤝 Contributing

Found a better approach? Submit a PR!

---

**Built for:** Kibana CSV automation testing  
**Tested on:** Elastic Demo Environment (demo.elastic.co)  
**Date:** 2026-02-02
