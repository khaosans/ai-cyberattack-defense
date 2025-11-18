#!/usr/bin/env python3
"""
Screenshot Capture Script for Dashboard Documentation
Captures screenshots of the dashboard in various states
"""
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Try to import playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Install with: pip install playwright && playwright install chromium")

# Try selenium as fallback
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


def create_screenshots_dir():
    """Create screenshots directory"""
    # Get project root (parent of scripts directory)
    project_root = Path(__file__).parent.parent
    screenshots_dir = project_root / "docs" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    return screenshots_dir


def wait_for_dashboard(url="http://localhost:8501", timeout=30):
    """Wait for dashboard to be ready"""
    import urllib.request
    import urllib.error
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except (urllib.error.URLError, OSError):
            time.sleep(1)
    return False


def capture_with_playwright(screenshots_dir: Path, base_url: str = "http://localhost:8501"):
    """Capture screenshots using Playwright"""
    print("📸 Using Playwright to capture screenshots...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Set viewport size
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        try:
            # Navigate to dashboard
            print(f"  → Navigating to {base_url}...")
            page.goto(base_url, wait_until="networkidle", timeout=30000)
            time.sleep(3)  # Wait for initial render
            
            # Screenshot 1: Initial Dashboard State
            print("  → Capturing initial dashboard state...")
            page.screenshot(path=str(screenshots_dir / "01_dashboard_initial.png"), full_page=True)
            
            # Screenshot 2: Start Simulation (click start button)
            print("  → Starting simulation...")
            start_button = page.locator("button:has-text('Start Simulation')")
            if start_button.count() > 0:
                start_button.first.click()
                time.sleep(2)
                page.screenshot(path=str(screenshots_dir / "02_dashboard_simulation_started.png"), full_page=True)
            
            # Screenshot 3: After some detections (wait for data)
            print("  → Waiting for detections...")
            time.sleep(5)
            page.screenshot(path=str(screenshots_dir / "03_dashboard_with_detections.png"), full_page=True)
            
            # Screenshot 4: Trigger Test Attack
            print("  → Triggering test attack...")
            test_attack_button = page.locator("button:has-text('Test Attack')")
            if test_attack_button.count() > 0:
                test_attack_button.first.click()
                time.sleep(3)
                page.screenshot(path=str(screenshots_dir / "04_dashboard_attack_detected.png"), full_page=True)
            
            # Screenshot 5: Charts view (scroll to charts)
            print("  → Capturing charts section...")
            page.evaluate("window.scrollTo(0, 400)")
            time.sleep(1)
            page.screenshot(path=str(screenshots_dir / "05_dashboard_charts.png"), full_page=True)
            
            # Screenshot 6: Alerts section
            print("  → Capturing alerts section...")
            page.evaluate("window.scrollTo(0, 800)")
            time.sleep(1)
            page.screenshot(path=str(screenshots_dir / "06_dashboard_alerts.png"), full_page=True)
            
            print("✅ Screenshots captured successfully!")
            
        except Exception as e:
            print(f"❌ Error capturing screenshots: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()


def capture_with_selenium(screenshots_dir: Path, base_url: str = "http://localhost:8501"):
    """Capture screenshots using Selenium (fallback)"""
    print("📸 Using Selenium to capture screenshots...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print(f"  → Navigating to {base_url}...")
        driver.get(base_url)
        time.sleep(3)
        
        # Screenshot 1: Initial state
        driver.save_screenshot(str(screenshots_dir / "01_dashboard_initial.png"))
        
        # Screenshot 2: After starting simulation
        try:
            start_button = driver.find_element("xpath", "//button[contains(text(), 'Start Simulation')]")
            start_button.click()
            time.sleep(2)
            driver.save_screenshot(str(screenshots_dir / "02_dashboard_simulation_started.png"))
        except:
            pass
        
        # Screenshot 3: With detections
        time.sleep(5)
        driver.save_screenshot(str(screenshots_dir / "03_dashboard_with_detections.png"))
        
        print("✅ Screenshots captured successfully!")
        
    except Exception as e:
        print(f"❌ Error capturing screenshots: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()


def create_manual_instructions(screenshots_dir: Path):
    """Create manual screenshot instructions"""
    instructions = f"""# Manual Screenshot Instructions

## Prerequisites
1. Start the dashboard: `streamlit run dashboard/app.py`
2. Wait for it to load at http://localhost:8501
3. Open the dashboard in your browser

## Screenshots to Capture

### 1. Initial Dashboard State
- **File**: `01_dashboard_initial.png`
- **Description**: Dashboard on first load, before starting simulation
- **Steps**: 
  1. Open dashboard
  2. Take full-page screenshot

### 2. Simulation Started
- **File**: `02_dashboard_simulation_started.png`
- **Description**: Dashboard with simulation running
- **Steps**:
  1. Click "▶️ Start Simulation"
  2. Wait 2 seconds
  3. Take full-page screenshot

### 3. With Detections
- **File**: `03_dashboard_with_detections.png`
- **Description**: Dashboard showing detected threats
- **Steps**:
  1. Let simulation run for 10-15 seconds
  2. Ensure some threats are detected
  3. Take full-page screenshot

### 4. Attack Detected
- **File**: `04_dashboard_attack_detected.png`
- **Description**: Dashboard after triggering test attack
- **Steps**:
  1. Click "🚀 Test Attack" button
  2. Wait for alerts to appear
  3. Take full-page screenshot

### 5. Charts Section
- **File**: `05_dashboard_charts.png`
- **Description**: Visualizations (timeline, gauge, distribution)
- **Steps**:
  1. Scroll to charts section
  2. Ensure charts are visible
  3. Take screenshot of charts area

### 6. Alerts Section
- **File**: `06_dashboard_alerts.png`
- **Description**: Recent alerts and threat details
- **Steps**:
  1. Scroll to alerts section
  2. Ensure alerts are visible
  3. Take screenshot of alerts area

## Screenshot Tips
- Use full-page screenshots when possible
- Ensure browser zoom is at 100%
- Use a modern browser (Chrome, Firefox, Safari)
- Capture at 1920x1080 resolution if possible
- Save screenshots in `docs/screenshots/` directory

## Browser Extensions
- Chrome: Use "Full Page Screen Capture" extension
- Firefox: Use "FireShot" extension
- Safari: Use Cmd+Shift+4 for selection, or Cmd+Shift+3 for full screen

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(screenshots_dir / "MANUAL_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print(f"📝 Manual instructions saved to {screenshots_dir / 'MANUAL_INSTRUCTIONS.md'}")


def main():
    """Main function"""
    print("=" * 70)
    print("Dashboard Screenshot Capture")
    print("=" * 70)
    print()
    
    # Check if dashboard is running
    print("🔍 Checking if dashboard is running...")
    if not wait_for_dashboard():
        print("❌ Dashboard not running!")
        print("   Please start it first: streamlit run dashboard/app.py")
        print()
        print("   Creating manual instructions instead...")
        screenshots_dir = create_screenshots_dir()
        create_manual_instructions(screenshots_dir)
        return 1
    
    print("✅ Dashboard is running!")
    print()
    
    # Create screenshots directory
    screenshots_dir = create_screenshots_dir()
    print(f"📁 Screenshots will be saved to: {screenshots_dir}")
    print()
    
    # Try to capture screenshots
    if PLAYWRIGHT_AVAILABLE:
        capture_with_playwright(screenshots_dir)
    elif SELENIUM_AVAILABLE:
        capture_with_selenium(screenshots_dir)
    else:
        print("⚠️  No browser automation available.")
        print("   Creating manual instructions...")
        create_manual_instructions(screenshots_dir)
        print()
        print("   To enable automated screenshots:")
        print("   - Install Playwright: pip install playwright && playwright install chromium")
        print("   - Or install Selenium: pip install selenium")
        return 1
    
    print()
    print("=" * 70)
    print("✅ Screenshot capture complete!")
    print(f"📁 Screenshots saved to: {screenshots_dir}")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

