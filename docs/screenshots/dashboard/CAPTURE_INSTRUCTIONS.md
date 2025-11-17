# Dashboard Screenshot Capture Instructions

To capture the dashboard screenshots described in the README, follow these steps:

## Prerequisites

1. Start the dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```
2. Open the dashboard in your browser (usually `http://localhost:8501`)

## Screenshots to Capture

### 1. Main Dashboard (`main-dashboard.png`)
**Already captured** - Using `image/README/1763411189376.png`

### 2. Pattern Distribution (`pattern-distribution.png`)

**What to capture:**
- Navigate to the "Attack Pattern Distribution" view
- Capture the full view showing:
  - Bar chart at top with pattern types (normal, behavioral_anomaly, superhuman_speed, systematic_enumeration)
  - Recent Alerts section (bottom-left) with alert cards
  - Recent Detections table (bottom-right)

**Steps:**
1. Start simulation if not already running
2. Trigger an attack to generate patterns
3. Navigate to pattern distribution view
4. Capture screenshot
5. Save as `docs/screenshots/dashboard/pattern-distribution.png`

### 3. Security Assistant (`security-assistant.png`)

**What to capture:**
- Open the "Ask Security Assistant" interface
- Type a question like "explain the charts"
- Capture the interface showing:
  - "Ask Security Assistant" header
  - User query input field
  - AI response explaining charts (GTG-1002 Campaign Timeline, Attack Patterns)

**Steps:**
1. Click on "Ask Security Assistant" or navigate to security assistant section
2. Enter a query: "explain the charts"
3. Wait for AI response
4. Capture screenshot showing the full conversation
5. Save as `docs/screenshots/dashboard/security-assistant.png`

### 4. Threat Detection Overview (`threat-detection-overview.png`)

**What to capture:**
- Can use the main dashboard view OR capture a comprehensive overview
- Should show multiple detection features together

**Steps:**
1. Use main dashboard screenshot OR
2. Capture a comprehensive view showing multiple detection features
3. Save as `docs/screenshots/dashboard/threat-detection-overview.png`

## Image Optimization

After capturing, optimize images:

```bash
# Using ImageMagick (if installed)
convert input.png -quality 85 -resize 1600x output.png

# Or use online tools like TinyPNG
```

## File Naming

Ensure files are named exactly:
- `main-dashboard.png`
- `pattern-distribution.png`
- `security-assistant.png`
- `threat-detection-overview.png`

## Verification

After adding images, verify they display correctly in README:
1. Check file paths in README.md
2. View README on GitHub
3. Ensure images load properly

