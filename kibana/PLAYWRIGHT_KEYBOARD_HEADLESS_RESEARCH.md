# 🎹 Playwright Keyboard Navigation in Headless Mode - Research

## ✅ TL;DR - No Additional Libraries Needed!

**Keyboard navigation works perfectly in Playwright headless mode with ZERO additional libraries.**

All keyboard methods (`page.keyboard.press()`, `page.keyboard.type()`, Tab navigation, etc.) are **built into Playwright** and work identically in both:
- ✅ Headless mode (`headless=True`)
- ✅ Headed mode (`headless=False`)

---

## 📚 Built-in Keyboard API

Playwright's `page.keyboard` API provides everything you need:

### Basic Key Presses

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # HEADLESS WORKS!
    page = browser.new_page()
    page.goto("https://example.com")
    
    # Single key press
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.keyboard.press("Escape")
    
    # Arrow keys
    page.keyboard.press("ArrowDown")
    page.keyboard.press("ArrowUp")
    
    # Modifiers
    page.keyboard.press("Control+A")
    page.keyboard.press("Shift+Tab")
    
    browser.close()
```

### Tab Navigation (Your Use Case)

```python
# Navigate through focusable elements
for i in range(10):
    page.keyboard.press("Tab")
    time.sleep(0.5)  # Optional: wait between tabs
    
    # Check what element is focused
    focused = page.evaluate("document.activeElement.tagName")
    print(f"Tab {i}: Focused on {focused}")
```

### Typing Text

```python
# Type slowly (simulates human typing)
page.keyboard.type("Hello World", delay=100)  # 100ms between keys

# Type instantly
page.keyboard.type("Fast typing")
```

### Key Down/Up (Advanced)

```python
# Hold Shift while pressing arrow keys
page.keyboard.down("Shift")
page.keyboard.press("ArrowRight")
page.keyboard.press("ArrowRight")
page.keyboard.up("Shift")
```

---

## 🔍 How It Works in Headless Mode

### Browser Event Simulation

Playwright doesn't "emulate" keyboard events - it **dispatches real browser events** through the Chrome DevTools Protocol (CDP):

1. **Your script:** `page.keyboard.press("Tab")`
2. **Playwright sends CDP command:** `Input.dispatchKeyEvent`
3. **Chromium processes real keyboard event:** Focus moves to next element
4. **Works identically** whether browser window is visible or not

### Why Headless Works Perfectly

Headless browsers are **full browsers without a graphical display**:
- ✅ Complete DOM rendering
- ✅ JavaScript execution
- ✅ Event handling (including keyboard events)
- ✅ Focus management
- ❌ Only missing: visual pixels on screen

**Result:** Keyboard API works exactly the same!

---

## 🧪 Testing Tab Navigation in Your Kibana Script

Your existing script should work in headless mode WITHOUT changes:

### Current Code (from `kibana_csv_keyboard.py`):

```python
# This works in BOTH headed and headless!
page.keyboard.press("PageDown")
page.keyboard.press("Tab")
page.keyboard.press("Enter")
page.keyboard.press("Escape")
```

### To Run in Headless Mode:

**Change this line:**
```python
browser = p.chromium.launch(headless=False)  # ← Currently headed
```

**To this:**
```python
browser = p.chromium.launch(headless=True)   # ← Headless for CI
```

**Everything else stays the same!**

---

## 📦 Libraries Comparison

### ❌ You DON'T Need These:

| Library | Why You Don't Need It |
|---------|----------------------|
| `pynput` | Desktop automation (controls your actual OS keyboard) - not for browsers |
| `keyboard` | Same as pynput - OS-level, not browser |
| `pyautogui` | Screen-based automation - requires visible window |
| `selenium.webdriver.common.keys` | Only needed if using Selenium instead of Playwright |

### ✅ You ONLY Need:

```bash
pip install playwright
playwright install chromium
```

That's it!

---

## 🎯 Real-World Example: Tab Through Panel Buttons

Here's how tab navigation works in your Kibana use case:

```python
from playwright.sync_api import sync_playwright
import time

def find_csv_button_with_tab():
    """
    Tab through all buttons until we find one with 'Download CSV' option.
    Works in headless mode!
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # HEADLESS!
        page = browser.new_page()
        
        page.goto("https://demo.elastic.co/app/dashboards#/view/...")
        time.sleep(10)  # Wait for load
        
        # Scroll to panel area
        for _ in range(5):
            page.keyboard.press("PageDown")
            time.sleep(0.5)
        
        # Tab through buttons
        print("🔍 Tabbing through buttons to find panel options...")
        for i in range(50):  # Try up to 50 tabs
            page.keyboard.press("Tab")
            time.sleep(0.3)
            
            # Check what's focused
            focused_text = page.evaluate("""
                const el = document.activeElement;
                return el ? el.textContent : '';
            """)
            
            print(f"Tab {i}: {focused_text[:50]}...")
            
            # If it's a panel options button, press Enter
            if "Panel options" in focused_text or "Options menu" in focused_text:
                print(f"✅ Found panel options at tab {i}! Opening...")
                page.keyboard.press("Enter")
                time.sleep(1)
                
                # Check if "Download CSV" is visible
                if page.locator('text="Download CSV"').count() > 0:
                    print("✅ Found Download CSV option!")
                    page.keyboard.press("ArrowDown")  # Navigate to it
                    page.keyboard.press("ArrowDown")
                    page.keyboard.press("Enter")  # Click it
                    
                    # Handle download
                    with page.expect_download() as download_info:
                        pass  # Download already triggered
                    
                    download = download_info.value
                    print(f"✅ Downloaded: {download.suggested_filename}")
                    break
                else:
                    # Wrong menu, close and continue
                    page.keyboard.press("Escape")
                    continue
        
        browser.close()

if __name__ == "__main__":
    find_csv_button_with_tab()
```

**This script runs identically in headless and headed modes!**

---

## 🐛 Common Gotchas (Not Library Issues)

### 1. Timing Issues

**Problem:** Elements not loaded when Tab is pressed

**Solution:** Add waits
```python
page.wait_for_load_state("networkidle")
time.sleep(2)  # Extra buffer
```

### 2. Dynamic Content

**Problem:** Tab order changes as page loads

**Solution:** Wait for specific element before tabbing
```python
page.wait_for_selector('[data-test-subj="dashboardGrid"]')
```

### 3. Focus Traps

**Problem:** Tab gets stuck in a modal or dropdown

**Solution:** Detect and escape
```python
# Check if we're in a modal
in_modal = page.evaluate("document.querySelector('[role=dialog]') !== null")
if in_modal:
    page.keyboard.press("Escape")
```

### 4. Tab Index Skips

**Problem:** Some elements aren't focusable

**Solution:** This is normal! Not all elements accept focus (divs, spans, etc.)

---

## 🚀 Performance in Headless Mode

### Benefits of Headless:

1. **Faster startup** (~2x faster without rendering UI)
2. **Lower memory** (no GPU rendering)
3. **Better for CI/CD** (no display server needed)
4. **Parallel execution** (run multiple browsers easily)

### Benchmarks (approximate):

| Mode | Browser Launch | Page Load | Total Time |
|------|---------------|-----------|------------|
| Headed | 3-5 seconds | 5-10 seconds | 8-15 seconds |
| Headless | 1-2 seconds | 4-8 seconds | 5-10 seconds |

**Keyboard navigation speed:** Identical in both modes!

---

## 📊 Debugging Headless Keyboard Navigation

### Option 1: Screenshots

```python
page.keyboard.press("Tab")
page.screenshot(path=f"tab_step_{i}.png")  # Visual checkpoint
```

### Option 2: Log Focused Element

```python
focused = page.evaluate("""
    const el = document.activeElement;
    return {
        tag: el.tagName,
        id: el.id,
        class: el.className,
        text: el.textContent.substring(0, 50)
    };
""")
print(f"Focused: {focused}")
```

### Option 3: Video Recording

```python
context = browser.new_context(record_video_dir="videos/")
# ... run your script ...
context.close()
# Video saved even in headless mode!
```

### Option 4: Playwright Inspector (Headed Only for Debugging)

```python
# For debugging only - use headed mode
browser = p.chromium.launch(headless=False, slow_mo=500)
# Each action slowed down by 500ms
```

---

## 🎬 GitLab CI Example with Keyboard Navigation

```yaml
kibana_export:
  image: mcr.microsoft.com/playwright/python:v1.41.0-jammy
  script:
    - pip install playwright
    # Script uses keyboard.press() in HEADLESS mode
    - python kibana_csv_keyboard.py
  artifacts:
    paths:
      - downloads/*.csv
      - screenshots/*.png  # Debug screenshots
```

**No special configuration needed for keyboard to work!**

---

## 🔬 Advanced: Custom Keyboard Sequences

### Macro-like Sequences

```python
def tab_and_check(page, count, target_text):
    """Tab N times and check for target text in focused element."""
    for i in range(count):
        page.keyboard.press("Tab")
        time.sleep(0.2)
        
        focused_text = page.evaluate("document.activeElement.textContent")
        if target_text in focused_text:
            return i
    return -1

# Usage
tab_count = tab_and_check(page, 50, "Panel options")
if tab_count >= 0:
    print(f"Found target after {tab_count} tabs")
```

### Keyboard Shortcut Combos

```python
# Ctrl+A (Select all)
page.keyboard.press("Control+A")

# Ctrl+C (Copy)
page.keyboard.press("Control+C")

# Multiple modifiers
page.keyboard.press("Control+Shift+P")  # Command palette

# Mac-specific (use Meta for Cmd)
page.keyboard.press("Meta+V")  # Cmd+V on Mac
```

---

## 📖 Official Documentation

**Playwright Keyboard API:**
- https://playwright.dev/python/docs/api/class-keyboard

**Key Values:**
- https://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_key_values

**Common Keys:**
- `Tab`, `Enter`, `Escape`, `Backspace`, `Delete`
- `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`
- `Home`, `End`, `PageUp`, `PageDown`
- `F1` through `F12`
- `Control`, `Shift`, `Alt`, `Meta` (modifiers)

---

## ✅ Summary

### Do You Need Additional Libraries for Keyboard Navigation in Headless Playwright?

**NO!** ❌

### What You Actually Need:

```bash
pip install playwright
playwright install chromium
```

### Your Existing Code:

```python
page.keyboard.press("Tab")
page.keyboard.press("Enter")
page.keyboard.press("Escape")
```

### Works In:

- ✅ Headed mode (browser visible)
- ✅ Headless mode (no window)
- ✅ GitLab CI/CD
- ✅ Docker containers
- ✅ Linux servers (no GUI)
- ✅ Windows/Mac/Linux

### Performance:

- ⚡ Identical keyboard event handling
- ⚡ Slightly faster in headless
- ⚡ Lower memory usage in headless

### Conclusion:

**Just change `headless=False` to `headless=True` in your script. Everything else works as-is!**

---

## 🎯 Action Items for Your GitLab Pipeline

1. ✅ Keep using `page.keyboard.press("Tab")` - no changes needed
2. ✅ Change `headless=False` to `headless=True` for CI
3. ✅ Add screenshots for debugging: `page.screenshot(path="debug.png")`
4. ✅ Add timing buffers: `time.sleep(0.5)` after Tab presses
5. ✅ Use `.gitlab-ci.yml` template provided earlier

**No additional libraries required!** 🎉
