# Demo Verification Checklist

## Purpose

This document provides a step-by-step verification checklist to ensure the AI Pattern Detector demo works correctly end-to-end.

## Pre-Verification Setup

### Environment Check

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Virtual environment created: `python3 -m venv venv`
- [ ] Virtual environment activated: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
- [ ] Dependencies installed: `pip install -r ai_tools/requirements.txt`
- [ ] No import errors: `python -c "import ai_tools; print('OK')"`
- [ ] Streamlit installed: `streamlit --version`

### Optional: Ollama Setup (for AI features)

- [ ] Ollama installed: `ollama --version`
- [ ] Ollama running: `ollama list` (should not error)
- [ ] Model pulled: `ollama pull llama3`
- [ ] Model verified: `ollama list` shows llama3

### File Structure Check

- [ ] `ai_tools/` directory exists
- [ ] `dashboard/` directory exists
- [ ] `docs/` directory exists
- [ ] All Python files present
- [ ] Configuration files present

---

## Verification Steps

### V1: Basic Installation Verification

**Command**: `python -c "from ai_tools.detection.ai_pattern_detector import AIPatternDetector; print('OK')"`

**Expected**: No errors, prints "OK"

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

---

### V2: Dashboard Startup

**Command**: `streamlit run dashboard/app.py`

**Steps**:
1. Run command
2. Wait for browser to open automatically
3. Verify dashboard loads

**Expected**:
- Browser opens at `http://localhost:8501`
- Dashboard header visible: "AI Pattern Detector Dashboard"
- Sidebar visible with controls
- Main content area visible
- No errors in terminal

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

**Screenshot**: (optional)

---

### V3: Sidebar Controls

**Steps**:
1. Verify sidebar contains:
   - Simulation controls (Start/Stop)
   - Attack controls (Trigger/Stop)
   - AI Features toggle
   - Configuration sliders
   - Reset button
   - Export button

**Expected**: All controls visible and accessible

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

---

### V4: Normal Traffic Simulation

**Steps**:
1. Click "Start Simulation" button
2. Observe metrics panel updates
3. Check threat timeline chart
4. Review recent detections table

**Expected**:
- Simulation starts (button disabled, Stop enabled)
- Metrics show increasing counts
- Timeline shows low-threat indicators (green)
- Detections appear in table
- Threat scores mostly < 30

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

**Duration**: Run for 30 seconds

---

### V5: Attack Traffic Simulation

**Steps**:
1. Ensure simulation is running
2. Click "Trigger Attack" button
3. Observe changes in:
   - Alert feed
   - Threat scores
   - Pattern types
   - Threat level

**Expected**:
- Attack triggers successfully
- Alerts appear in alert feed
- Threat scores increase (> 50)
- Pattern types show: superhuman_speed, systematic_enumeration, or behavioral_anomaly
- Threat levels change to "suspicious" or "malicious"
- Timeline shows higher threat indicators (orange/red)

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

**Duration**: Run for 30 seconds

---

### V6: Visualizations Rendering

**Steps**:
1. Verify all charts render:
   - Threat Timeline
   - Threat Gauge
   - Pattern Distribution

**Expected**:
- All charts visible
- Charts update in real-time
- No rendering errors
- Data displays correctly

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

---

### V7: AI Features - Ollama Available

**Prerequisites**: Ollama installed and running

**Steps**:
1. Check "Enable AI Analysis" checkbox
2. Verify Ollama status shows "Connected"
3. Verify model name displayed
4. Generate attack traffic
5. Click "AI Insights" on an alert
6. Verify AI analysis panel appears
7. Check Security Assistant Q&A

**Expected**:
- Ollama status: "Connected"
- Model name shown (e.g., "llama3")
- AI Insights panel displays explanations
- Intent classification shown
- Recommendations appear
- Security Assistant answers questions

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

---

### V8: AI Features - Ollama Unavailable

**Prerequisites**: Ollama NOT running

**Steps**:
1. Ensure Ollama is stopped
2. Check "Enable AI Analysis" checkbox
3. Verify Ollama status shows "Unavailable"
4. Start simulation
5. Trigger attack
6. Verify detections still work
7. Check alerts display (without AI)

**Expected**:
- Ollama status: "Unavailable"
- System continues functioning
- Rule-based detection works
- Basic threat explanations provided
- No errors or crashes

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

---

### V9: Configuration Changes

**Steps**:
1. Adjust "Superhuman Speed Threshold" slider
2. Adjust "Attack Intensity" slider
3. Observe detection sensitivity changes
4. Reset to defaults

**Expected**:
- Sliders work correctly
- Threshold changes affect detection
- Attack intensity affects traffic mix
- Reset restores defaults

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

---

### V10: Export Functionality

**Steps**:
1. Generate detections (normal + attack)
2. Click "Export Detections" button
3. Download CSV file
4. Open CSV file
5. Verify data structure

**Expected**:
- CSV downloads successfully
- File contains detection data
- Columns present: timestamp, threat_score, threat_level, pattern_type, endpoint, IP
- Data matches dashboard

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

**File Name**: `detections_YYYYMMDD_HHMMSS.csv`

---

### V11: Reset Functionality

**Steps**:
1. Generate detections
2. Verify metrics show counts
3. Click "Reset Detector" button
4. Verify metrics reset
5. Check charts reset

**Expected**:
- Reset clears all detections
- Metrics return to zero
- Charts reset
- Alert feed clears
- No errors

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

---

### V12: Error Handling

**Steps**:
1. Test invalid configurations
2. Stop Ollama during operation (if running)
3. Verify graceful degradation
4. Test with missing dependencies

**Expected**:
- Errors handled gracefully
- No crashes
- Error messages informative
- System recovers

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

---

### V13: Performance

**Steps**:
1. Run simulation for 5+ minutes
2. Monitor memory usage
3. Check response times
4. Verify no slowdowns

**Expected**:
- Dashboard remains responsive
- Memory usage stable
- No performance degradation
- Charts update smoothly

**Status**: [ ] PASS [ ] FAIL

**Notes**: 

**Memory Usage**: _____ MB
**Response Time**: _____ ms

---

## Verification Summary

### Overall Status

- [ ] All tests PASSED
- [ ] Some tests FAILED (see notes)
- [ ] Tests BLOCKED (see notes)

### Critical Issues

List any critical issues found:

1. 
2. 
3. 

### Minor Issues

List any minor issues found:

1. 
2. 
3. 

### Recommendations

1. 
2. 
3. 

---

## Test Environment

- **Date**: YYYY-MM-DD
- **Tester**: Name
- **OS**: 
- **Python Version**: 
- **Browser**: 
- **Ollama Version**: (if applicable)
- **Ollama Model**: (if applicable)

## Sign-off

- **Verified By**: ________________
- **Date**: ________________
- **Status**: [ ] APPROVED [ ] NEEDS WORK

---

**Last Updated**: 2025-01-XX
**Version**: 1.0

