# Dashboard Screenshot Sources

This document tracks the source and usage of dashboard screenshots.

## Required Images

Based on the dashboard interface, we need the following screenshots:

### 1. Main Dashboard (`main-dashboard.png`)
**Description:** Main threat analysis dashboard showing:
- Left sidebar with simulation controls, AI features (Ollama status), and configuration
- Threat Timeline section
- Threat Level Gauge (semi-circular gauge showing current threat level)
- Threat Score Timeline (line graph with thresholds)
- Pattern Distribution section

**Source:** `image/README/1763411189376.png` (copied)

### 2. Pattern Distribution (`pattern-distribution.png`)
**Description:** Attack pattern distribution view showing:
- Bar chart at top with pattern types: normal, behavioral_anomaly, superhuman_speed, systematic_enumeration
- Recent Alerts section (bottom-left) with alert cards
- Recent Detections table (bottom-right) with detection history

**Status:** Needs to be captured from dashboard

### 3. Security Assistant (`security-assistant.png`)
**Description:** AI Security Assistant chat interface showing:
- "Ask Security Assistant" header
- User query input field
- AI response explaining charts (GTG-1002 Campaign Timeline, Attack Patterns)
- Dark-themed chat interface

**Status:** Needs to be captured from dashboard

### 4. Threat Detection Overview (`threat-detection-overview.png`)
**Description:** Comprehensive overview of threat detection features
- Can use main dashboard or a different comprehensive view

**Status:** Can use main dashboard or capture specific overview

## How to Capture New Screenshots

1. Start the dashboard: `streamlit run dashboard/app.py`
2. Navigate to the specific view you want to capture
3. Take a screenshot (Cmd+Shift+4 on macOS, or use screenshot tool)
4. Save with the appropriate filename in `docs/screenshots/dashboard/`
5. Optimize if needed (reduce file size while maintaining quality)

## Current Status

- ✅ Main dashboard image saved
- ⏳ Pattern distribution - needs capture
- ⏳ Security assistant - needs capture  
- ⏳ Threat detection overview - can use main or capture

