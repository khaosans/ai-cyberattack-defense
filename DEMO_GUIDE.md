# Dashboard Demo Guide

Complete step-by-step guide for demonstrating the AI Pattern Detector Dashboard.

## Quick Start

1. **Start the Dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```
   Dashboard will open at: http://localhost:8501

2. **Run Automated Demo** (optional):
   ```bash
   python3 tools/demo_dashboard.py
   ```

## Demo Workflow

### Phase 1: Initial Setup (30 seconds)

1. **Verify Dashboard Loads**
   - Open http://localhost:8501
   - Check sidebar appears on left
   - Verify main dashboard area shows metrics (all zeros initially)

2. **Check Database Status**
   - Look at sidebar "💾 Database" section
   - Note total detections count
   - Check Vector DB status (may show "Not available" if ChromaDB not installed)

### Phase 2: Quick Test Attack (1 minute)

1. **Use Test Attack Button**
   - In sidebar, find "🚀 Test Attack" button
   - Click it
   - Watch for: "Test attack in progress... (X/20 requests)"
   - Wait for completion message

2. **Verify Detections Appear**
   - Check metrics update: Total Detections should increase
   - Look for threat detection banners (red/yellow)
   - Verify charts populate with data
   - Check alert feed shows threats

### Phase 3: Full Simulation Demo (2-3 minutes)

1. **Start Simulation**
   - Click "▶️ Start Simulation" button
   - Set "Attack Intensity" slider to 0.5 or higher
   - Verify "🔴 Attack Mode Active" message appears

2. **Monitor Real-Time Detection**
   - Watch request counter increment
   - Observe metrics updating with delta indicators
   - Check threat timeline chart updates
   - Verify threat gauge shows current level
   - Watch alert feed populate

3. **Verify Threat Detection**
   - After 10-15 requests, threats should appear
   - Look for red/yellow threat banners
   - Check "Malicious Threats" metric increases
   - Verify alerts show in alert feed

### Phase 4: Database Features (1 minute)

1. **Check Database Persistence**
   - Note current detection count in sidebar
   - Refresh browser page (F5)
   - Verify detections persist (count remains)
   - Check "Reload from DB" button works

2. **Test Database Stats**
   - Verify stats show correct counts
   - Check breakdown: Malicious/Suspicious/Normal
   - Test "Clear Old" button (if needed)

### Phase 5: Vector Database Features (if ChromaDB installed) (1 minute)

1. **Test Similarity Search**
   - Find a threat alert in the alert feed
   - Click "🔍 Find Similar" button
   - Verify similar attacks panel appears
   - Check similar attacks are displayed

2. **View Threat Clusters**
   - Scroll to "📊 Threat Clusters" expandable section
   - Expand it
   - Verify clusters are shown (if enough data)
   - Check cluster information displays correctly

### Phase 6: UI Components Verification (1 minute)

1. **Charts**
   - Threat Timeline: Should show colored dots (green/orange/red)
   - Threat Gauge: Should show current threat level
   - Pattern Distribution: Should show bar chart of patterns

2. **Metrics**
   - Total Detections: Should increment
   - Malicious Threats: Should show count with delta
   - Avg Threat Score: Should calculate correctly
   - Peak Threat Score: Should show maximum

3. **Alert Feed**
   - Should show recent threats
   - Color coding: 🔴 High, 🟡 Medium
   - Timestamps should display
   - AI Insights button available (if AI enabled)

4. **Recent Detections Table**
   - Should show 10 most recent detections
   - Columns: Time, Threat Score, Level, Pattern, Endpoint, IP
   - Should update in real-time

### Phase 7: Export and Cleanup (30 seconds)

1. **Export Detections**
   - Click "📥 Export Detections" button
   - Verify CSV downloads
   - Check CSV contains detection data

2. **Reset (Optional)**
   - Click "🔄 Reset Detector"
   - Verify metrics reset to zero
   - Check database records preserved (message confirms)

## Expected Results

### After Test Attack (20 requests):
- **Total Detections**: ~20
- **Threats Detected**: 8-12 threats (suspicious/malicious)
- **Max Threat Score**: 40-90
- **Alerts Created**: 8-12 alerts
- **Charts**: All populated with data

### After Full Simulation (30+ requests):
- **Total Detections**: 30+
- **Threats Detected**: 15-25 threats
- **Patterns**: Mix of superhuman_speed, systematic_enumeration
- **Database**: All detections saved
- **Vector DB**: Embeddings created (if ChromaDB installed)

## Troubleshooting

### No Threats Detected?
- **Solution**: Increase attack intensity to 1.0
- **Solution**: Wait for 15+ requests (detector needs history)
- **Solution**: Use "🚀 Test Attack" for guaranteed threats

### Dashboard Not Updating?
- **Solution**: Ensure "Start Simulation" is clicked
- **Solution**: Check browser console for errors
- **Solution**: Refresh page (F5)

### Vector DB Not Available?
- **Solution**: Install ChromaDB: `pip install chromadb` or `python3 scripts/install_vector_db.py`
- **Note**: Dashboard works fine without vector DB features

### Performance Issues?
- **Solution**: Reduce attack intensity
- **Solution**: Clear old detections (>7 days)
- **Solution**: Limit displayed detections

## Demo Scripts

### Automated Demo
```bash
python3 tools/demo_dashboard.py
```
Runs all tests automatically and reports results.

### CLI Testing
```bash
# Quick attack test
python3 tools/cli_test.py attack --count 20

# Continuous test
python3 tools/cli_test.py continuous --duration 60 --intensity 0.7
```

## Key Features to Highlight

1. **Real-Time Detection**: Threats appear within seconds
2. **Batch Processing**: Fast request generation (5 per iteration)
3. **Database Persistence**: Detections survive refreshes
4. **Vector Similarity**: Find similar attacks (if ChromaDB installed)
5. **Visual Feedback**: Threat banners, delta indicators, request counter
6. **Export Capability**: Download detection logs

## Success Metrics

✅ Dashboard loads without errors
✅ Detections appear within 15 requests
✅ Threats are detected and displayed
✅ Database persists data correctly
✅ Charts render with data
✅ Alerts show in feed
✅ Metrics update in real-time
✅ Vector DB works (if installed)
✅ Export functionality works

## Demo Duration

- **Quick Demo**: 2-3 minutes (Test Attack + basic features)
- **Full Demo**: 5-7 minutes (All features + workflows)
- **Automated Demo**: 30 seconds (script runs all tests)

