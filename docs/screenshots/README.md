# Screenshots Directory

This directory contains visual documentation of the AI Pattern Detector dashboard.

## Screenshots Available

Screenshots are captured using `capture_screenshots.py` or manually following instructions in `MANUAL_INSTRUCTIONS.md`.

## Screenshot Files

- `01_dashboard_initial.png` - Dashboard on first load
- `02_dashboard_simulation_started.png` - Dashboard with simulation running
- `03_dashboard_with_detections.png` - Dashboard showing detected threats
- `04_dashboard_attack_detected.png` - Dashboard after triggering test attack
- `05_dashboard_charts.png` - Visualizations (timeline, gauge, distribution)
- `06_dashboard_alerts.png` - Recent alerts and threat details

## Capturing Screenshots

### Automated Capture
```bash
# Start dashboard first
streamlit run dashboard/app.py

# In another terminal, capture screenshots
python3 scripts/capture_screenshots.py
```

### Manual Capture
See `MANUAL_INSTRUCTIONS.md` for detailed manual screenshot instructions.

## Usage in Documentation

Screenshots are referenced in:
- `KEY_TAKEAWAYS_AND_FUTURE_WORK.md` - Demo and visual documentation section
- `docs/DEMO_OUTPUT.md` - Test results documentation
- `README.md` - Project overview


