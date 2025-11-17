# Test Plan - AI Pattern Detector

## Overview

This document provides comprehensive manual test procedures for the AI Pattern Detector system. It covers all features, components, and integration points.

## Test Environment Setup

### Prerequisites

1. Python 3.8 or higher installed
2. Virtual environment created and activated
3. All dependencies installed: `pip install -r ai_tools/requirements.txt`
4. Optional: Ollama installed and running (for AI features)

### Test Data

- Normal traffic patterns
- Attack traffic patterns (GTG-1002 style)
- Various endpoint patterns
- Different IP addresses
- Multiple user agents

## Test Scenarios

### TS-1: Installation and Setup

**Objective**: Verify system installs and configures correctly

**Steps**:
1. Clone repository
2. Create virtual environment: `python3 -m venv venv`
3. Activate virtual environment
4. Install dependencies: `pip install -r ai_tools/requirements.txt`
5. Verify installation: `python -c "import ai_tools; print('OK')"`

**Expected Results**:
- All dependencies install without errors
- No import errors
- System ready for use

**Test Data**: None required

---

### TS-2: Dashboard Startup

**Objective**: Verify dashboard starts and displays correctly

**Steps**:
1. Start dashboard: `streamlit run dashboard/app.py`
2. Wait for browser to open
3. Verify dashboard loads
4. Check sidebar is visible
5. Verify main content area displays

**Expected Results**:
- Dashboard opens at `http://localhost:8501`
- No errors in console
- All UI elements visible
- Metrics show zero/initial values

**Test Data**: None required

---

### TS-3: Normal Traffic Simulation

**Objective**: Verify normal traffic generation and detection

**Steps**:
1. Start dashboard
2. Click "Start Simulation" button
3. Observe traffic generation
4. Monitor metrics panel
5. Check threat timeline chart
6. Review recent detections table

**Expected Results**:
- Simulation starts successfully
- Requests generate continuously
- Metrics update in real-time
- Threat scores remain low (< 30)
- Most detections marked as "normal"
- Timeline shows green/low-threat indicators

**Test Data**: Normal traffic patterns

---

### TS-4: Attack Traffic Simulation

**Objective**: Verify attack detection capabilities

**Steps**:
1. Start dashboard
2. Click "Start Simulation"
3. Wait for normal traffic baseline (10-20 requests)
4. Click "Trigger Attack" button
5. Observe detection changes
6. Monitor alert feed
7. Check threat scores increase
8. Verify pattern types detected

**Expected Results**:
- Attack simulation triggers successfully
8. Threat scores increase significantly (> 50)
9. Alerts appear in alert feed
10. Pattern types include: superhuman_speed, systematic_enumeration, or behavioral_anomaly
11. Threat level changes to "suspicious" or "malicious"
12. Timeline shows orange/red indicators

**Test Data**: Attack traffic patterns

---

### TS-5: Superhuman Speed Detection

**Objective**: Verify superhuman speed pattern detection

**Steps**:
1. Start dashboard
2. Configure speed threshold: Set to 5 req/s in sidebar
3. Start simulation
4. Trigger attack
5. Monitor for speed detections
6. Check alert messages mention speed
7. Verify threat scores reflect speed detection

**Expected Results**:
- Speed detections appear in alerts
- Pattern type shows "superhuman_speed"
- Threat score increases (40+ points)
- Alert message describes speed anomaly

**Test Data**: Rapid request patterns (> 5 req/s)

---

### TS-6: Systematic Enumeration Detection

**Objective**: Verify enumeration pattern detection

**Steps**:
1. Start dashboard
2. Start simulation
3. Trigger attack
4. Monitor endpoint patterns
5. Look for sequential endpoint access
6. Check for enumeration alerts

**Expected Results**:
- Enumeration detections appear
- Pattern type shows "systematic_enumeration"
- Sequential endpoint patterns visible
- Threat score reflects enumeration (35+ points)

**Test Data**: Sequential endpoint patterns (/api/users/1, /api/users/2, etc.)

---

### TS-7: Behavioral Anomaly Detection

**Objective**: Verify anomaly detection capabilities

**Steps**:
1. Start dashboard
2. Start simulation
3. Allow normal traffic baseline
4. Trigger attack
5. Monitor for anomaly detections
6. Check statistical pattern analysis

**Expected Results**:
- Anomaly detections appear
- Pattern type shows "behavioral_anomaly"
- Unusual patterns identified
- Threat score reflects anomalies (25+ points)

**Test Data**: Unusual request patterns (deep paths, unusual parameters)

---

### TS-8: AI Features - With Ollama

**Objective**: Verify AI-enhanced features when Ollama is available

**Prerequisites**: Ollama installed and running

**Steps**:
1. Verify Ollama running: `ollama list`
2. Start dashboard
3. Check "Enable AI Analysis" checkbox in sidebar
4. Verify Ollama status shows "Connected"
5. Start simulation
6. Trigger attack
7. Click "AI Insights" button on an alert
8. Verify AI explanation appears
9. Check recommendations panel
10. Test Security Assistant Q&A

**Expected Results**:
- Ollama status shows "Connected"
- AI Insights panel displays
- Natural language explanations provided
- Intent classification shown
- Recommendations appear
- Security Assistant answers questions

**Test Data**: Attack detections with AI analysis

---

### TS-9: AI Features - Without Ollama (Graceful Degradation)

**Objective**: Verify system works without Ollama

**Prerequisites**: Ollama NOT running or disabled

**Steps**:
1. Ensure Ollama is not running
2. Start dashboard
3. Check "Enable AI Analysis" checkbox
4. Verify Ollama status shows "Unavailable"
5. Start simulation
6. Trigger attack
7. Verify detections still work
8. Check alerts display (without AI explanations)
9. Verify no errors occur

**Expected Results**:
- Ollama status shows "Unavailable"
- System continues to function
- Rule-based detection works
- No errors or crashes
- Basic threat explanations provided
- Recommendations panel may be empty or show basic recommendations

**Test Data**: Normal and attack traffic

---

### TS-10: Configuration Changes

**Objective**: Verify configuration adjustments work

**Steps**:
1. Start dashboard
2. Adjust "Superhuman Speed Threshold" slider
3. Adjust "Attack Intensity" slider
4. Start simulation
5. Observe detection sensitivity changes
6. Reset to defaults
7. Verify behavior returns to normal

**Expected Results**:
- Threshold changes affect detection sensitivity
- Lower threshold = more detections
- Higher threshold = fewer detections
- Attack intensity affects traffic mix
- Reset restores defaults

**Test Data**: Various threshold values

---

### TS-11: Export Functionality

**Objective**: Verify detection export works

**Steps**:
1. Start dashboard
2. Start simulation
3. Generate detections (normal + attack)
4. Click "Export Detections" button
5. Download CSV file
6. Open CSV in spreadsheet application
7. Verify data structure
8. Check all fields present

**Expected Results**:
- CSV file downloads successfully
- File contains detection data
- Columns include: timestamp, threat_score, threat_level, pattern_type, endpoint, IP
- Data matches dashboard display

**Test Data**: Multiple detections

---

### TS-12: Reset Functionality

**Objective**: Verify reset clears history

**Steps**:
1. Start dashboard
2. Start simulation
3. Generate detections
4. Verify metrics show detections
5. Click "Reset Detector" button
6. Verify metrics reset to zero
7. Check detection history cleared

**Expected Results**:
- Reset button clears all detections
- Metrics return to zero
- Charts reset
- Alert feed clears
- No errors occur

**Test Data**: Existing detections

---

### TS-13: Dashboard Performance

**Objective**: Verify dashboard handles high load

**Steps**:
1. Start dashboard
2. Start simulation
3. Let run for extended period (5+ minutes)
4. Monitor memory usage
5. Check response times
6. Verify no slowdowns
7. Test with 1000+ detections

**Expected Results**:
- Dashboard remains responsive
- Memory usage stable
- No performance degradation
- Charts update smoothly
- No crashes or errors

**Test Data**: High-volume traffic

---

### TS-14: Error Handling

**Objective**: Verify error handling and recovery

**Steps**:
1. Start dashboard
2. Start simulation
3. Stop Ollama (if running) during operation
4. Verify graceful degradation
5. Restart Ollama
6. Verify reconnection works
7. Test invalid configurations
8. Verify error messages display

**Expected Results**:
- Errors handled gracefully
- No crashes
- Error messages informative
- System recovers from errors
- Degradation works smoothly

**Test Data**: Error conditions

---

### TS-15: Cross-Browser Compatibility

**Objective**: Verify dashboard works in different browsers

**Steps**:
1. Test in Chrome
2. Test in Firefox
3. Test in Safari
4. Test in Edge
5. Verify all features work
6. Check visualizations render
7. Test interactions

**Expected Results**:
- Dashboard works in all browsers
- Visualizations render correctly
- No browser-specific errors
- Consistent behavior

**Test Data**: Multiple browsers

---

## Test Execution Checklist

- [ ] TS-1: Installation and Setup
- [ ] TS-2: Dashboard Startup
- [ ] TS-3: Normal Traffic Simulation
- [ ] TS-4: Attack Traffic Simulation
- [ ] TS-5: Superhuman Speed Detection
- [ ] TS-6: Systematic Enumeration Detection
- [ ] TS-7: Behavioral Anomaly Detection
- [ ] TS-8: AI Features - With Ollama
- [ ] TS-9: AI Features - Without Ollama
- [ ] TS-10: Configuration Changes
- [ ] TS-11: Export Functionality
- [ ] TS-12: Reset Functionality
- [ ] TS-13: Dashboard Performance
- [ ] TS-14: Error Handling
- [ ] TS-15: Cross-Browser Compatibility

## Test Results Template

For each test scenario, document:

- **Test ID**: TS-X
- **Date**: YYYY-MM-DD
- **Tester**: Name
- **Environment**: OS, Python version, Browser
- **Result**: PASS / FAIL / BLOCKED
- **Notes**: Any observations or issues
- **Screenshots**: If applicable

## Known Issues and Limitations

1. AI features require Ollama to be running
2. High request rates may impact performance
3. Some browsers may have rendering differences
4. Ollama connection status may take a moment to update

## Regression Testing

After code changes, re-run:
- TS-2: Dashboard Startup
- TS-3: Normal Traffic Simulation
- TS-4: Attack Traffic Simulation
- TS-8/TS-9: AI Features (both scenarios)

## Performance Benchmarks

- Dashboard startup: < 5 seconds
- Request processing: < 100ms per request
- Chart rendering: < 500ms
- AI analysis (if enabled): < 2 seconds per detection

---

**Last Updated**: 2025-01-XX
**Version**: 1.0

