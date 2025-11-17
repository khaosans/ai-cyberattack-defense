"""
AI Pattern Detector Dashboard
Streamlit dashboard for real-time threat detection visualization
"""
import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
from ai_tools.simulation.attack_simulator import AttackSimulator
from ai_tools.utils.models import Detection
from ai_tools.utils.database import DetectionDB
from ai_tools.config import Config
from ai_tools.ai_analysis.threat_analyzer import AIThreatAnalyzer
from ai_tools.ai_analysis.security_assistant import SecurityAssistant

# Import dashboard components
try:
    from dashboard.components.threat_chart import create_threat_timeline, create_pattern_distribution, create_threat_gauge
    from dashboard.components.alert_feed import create_alerts, get_alert_color, format_alert_time
    from dashboard.components.metrics_panel import get_metrics_summary
    from dashboard.components.ai_insights import (
        create_threat_explanation_card,
        create_ai_recommendations_panel,
        format_ai_alert,
        generate_attack_scenario_description
    )
    try:
        from dashboard.components.threat_correlation import (
            create_similar_attacks_panel,
            create_threat_cluster_panel
        )
    except ImportError:
        from components.threat_correlation import (
            create_similar_attacks_panel,
            create_threat_cluster_panel
        )
except ImportError:
    # Fallback for direct execution
    from components.threat_chart import create_threat_timeline, create_pattern_distribution, create_threat_gauge
    from components.alert_feed import create_alerts, get_alert_color, format_alert_time
    from components.metrics_panel import get_metrics_summary
    from components.ai_insights import (
        create_threat_explanation_card,
        create_ai_recommendations_panel,
        format_ai_alert,
        generate_attack_scenario_description
    )

# Page configuration
st.set_page_config(
    page_title="AI Pattern Detector - GTG-1002 Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state with robust error handling
if 'detector' not in st.session_state:
    startup_errors = []
    startup_warnings = []
    
    try:
        from ai_tools.utils.startup import StartupManager
        
        # Create startup manager
        startup_mgr = StartupManager()
        base_path = Path(__file__).parent.parent
        
        # Ensure directories exist
        if not startup_mgr.ensure_directories(base_path):
            startup_errors.extend(startup_mgr.status['errors'])
        
        config = Config()
        
        # Initialize detector with error handling
        try:
            st.session_state.detector = EnhancedAIPatternDetector(config=config, enable_ai=True)
        except Exception as e:
            startup_errors.append(f"Detector initialization failed: {e}")
            st.session_state.detector = None
        
        # Initialize simulator
        try:
            st.session_state.simulator = AttackSimulator()
        except Exception as e:
            startup_errors.append(f"Simulator initialization failed: {e}")
            st.session_state.simulator = None
        
        # Initialize session state variables
        st.session_state.running = False
        st.session_state.detections = []
        st.session_state.last_update = datetime.now()
        st.session_state.request_count = 0
        st.session_state.last_threat_detected = None
        st.session_state.prev_metrics = {}
        
        # Initialize database with robust error handling
        db_path = Path(__file__).parent.parent / "detections.db"
        
        # Validate database path
        db_valid, db_error = startup_mgr.validate_database(str(db_path))
        if not db_valid:
            startup_errors.append(f"Database validation failed: {db_error}")
        
        try:
            st.session_state.db = DetectionDB(str(db_path), enable_vector_db=True)
            st.session_state.vector_db_status = st.session_state.db.vector_db_status
            
            # Load recent detections from database
            try:
                recent_from_db = st.session_state.db.get_recent_detections(limit=100)
                st.session_state.detections = recent_from_db
                st.session_state.request_count = len(recent_from_db)
            except Exception as e:
                startup_warnings.append(f"Failed to load recent detections: {e}")
                st.session_state.detections = []
                st.session_state.request_count = 0
        except Exception as e:
            startup_errors.append(f"Database initialization failed: {e}")
            st.session_state.db = None
        
        # Initialize AI components with proper error handling
        st.session_state.ai_enabled = config.AI_ANALYSIS_ENABLED
        st.session_state.ai_analyzer = None
        st.session_state.security_assistant = None
        st.session_state.ollama_status = "checking"
        st.session_state.ollama_model = None
        
        if st.session_state.ai_enabled:
            try:
                st.session_state.ai_analyzer = AIThreatAnalyzer(config=config)
                st.session_state.security_assistant = SecurityAssistant(config=config)
                
                # Check Ollama connection status
                if st.session_state.ai_analyzer and st.session_state.ai_analyzer.ollama:
                    if st.session_state.ai_analyzer.ollama.is_available():
                        st.session_state.ollama_status = "connected"
                        st.session_state.ollama_model = st.session_state.ai_analyzer.ollama.model
                    else:
                        st.session_state.ollama_status = "unavailable"
                        startup_warnings.append("Ollama is not available")
                else:
                    st.session_state.ollama_status = "unavailable"
                    startup_warnings.append("AI analyzer not initialized")
            except Exception as e:
                st.session_state.ollama_status = "error"
                startup_warnings.append(f"AI features initialization warning: {e}")
        
        st.session_state.selected_detection = None
        st.session_state.startup_errors = startup_errors
        st.session_state.startup_warnings = startup_warnings
        
        # Only mark as initialized if critical components are ready
        if st.session_state.detector is not None and st.session_state.simulator is not None and st.session_state.db is not None:
            st.session_state.initialized = True
        else:
            st.session_state.initialized = False
            startup_errors.append("Critical components failed to initialize")
        
    except Exception as e:
        startup_errors.append(f"Startup failed: {e}")
        st.session_state.initialized = False
        st.session_state.startup_errors = startup_errors
        st.session_state.startup_warnings = startup_warnings

# Display startup errors/warnings if any
if st.session_state.get('startup_errors'):
    for error in st.session_state.startup_errors:
        st.error(f"⚠️ Startup Error: {error}")
    
    if not st.session_state.get('initialized', False):
        st.error("❌ Application failed to initialize. Some features may not work.")
        st.info("💡 Try refreshing the page or check the logs for more details.")

if st.session_state.get('startup_warnings'):
    with st.expander("ℹ️ Startup Warnings", expanded=False):
        for warning in st.session_state.startup_warnings:
            st.warning(warning)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #fee;
        border-left: 4px solid #e74c3c;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-medium {
        background-color: #fff8e1;
        border-left: 4px solid #f39c12;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-text {
        color: #333333;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .alert-details {
        color: #555555;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🛡️ AI Pattern Detector Dashboard</div>', unsafe_allow_html=True)
st.markdown("**Real-time detection of GTG-1002 style autonomous AI attacks**")

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Simulation controls
    st.subheader("Simulation")
    if st.button("▶️ Start Simulation", disabled=st.session_state.running):
        st.session_state.running = True
        st.session_state.simulator.stop_attack()
        st.rerun()
    
    if st.button("⏸️ Stop Simulation", disabled=not st.session_state.running):
        st.session_state.running = False
        st.rerun()
    
    if st.button("🎯 Trigger Attack", disabled=not st.session_state.running):
        st.session_state.simulator.start_attack()
        st.success("Attack simulation started!")
    
    if st.button("🛑 Stop Attack", disabled=not st.session_state.running):
        st.session_state.simulator.stop_attack()
        st.info("Attack simulation stopped.")
    
    st.divider()
    
    # AI Features Toggle
    st.subheader("🤖 AI Features")
    ai_enabled = st.checkbox(
        "Enable AI Analysis",
        value=st.session_state.ai_enabled,
        help="Enable Ollama LLM for enhanced threat analysis and explanations"
    )
    
    if ai_enabled != st.session_state.ai_enabled:
        st.session_state.ai_enabled = ai_enabled
        if ai_enabled:
            try:
                config = Config()
                st.session_state.ai_analyzer = AIThreatAnalyzer(config=config)
                st.session_state.security_assistant = SecurityAssistant(config=config)
                st.session_state.detector = EnhancedAIPatternDetector(config=config, enable_ai=True)
                
                # Update Ollama status
                if st.session_state.ai_analyzer and st.session_state.ai_analyzer.ollama:
                    if st.session_state.ai_analyzer.ollama.is_available():
                        st.session_state.ollama_status = "connected"
                        st.session_state.ollama_model = st.session_state.ai_analyzer.ollama.model
                    else:
                        st.session_state.ollama_status = "unavailable"
                else:
                    st.session_state.ollama_status = "unavailable"
            except Exception as e:
                st.session_state.ollama_status = "error"
                st.warning(f"AI initialization error: {e}")
        else:
            st.session_state.ai_analyzer = None
            st.session_state.security_assistant = None
            st.session_state.detector = EnhancedAIPatternDetector(config=Config(), enable_ai=False)
            st.session_state.ollama_status = "disabled"
        st.rerun()
    
    # Display Ollama status with proper checking
    if st.session_state.ai_enabled:
        # Check status from session state or re-check
        if hasattr(st.session_state, 'ollama_status'):
            status = st.session_state.ollama_status
        else:
            # Re-check if needed
            try:
                if st.session_state.ai_analyzer and st.session_state.ai_analyzer.ollama:
                    status = "connected" if st.session_state.ai_analyzer.ollama.is_available() else "unavailable"
                else:
                    status = "unavailable"
            except:
                status = "unavailable"
        
        # Display status with appropriate color
        if status == "connected":
            st.caption("🟢 **Ollama Status: Connected**")
            if st.session_state.ollama_model:
                st.caption(f"**Model:** {st.session_state.ollama_model}")
        elif status == "checking":
            st.caption("🟡 **Ollama Status: Checking...**")
        elif status == "error":
            st.caption("🔴 **Ollama Status: Error**")
        else:
            st.caption("🔴 **Ollama Status: Unavailable**")
            st.caption("_AI features will use fallback mode_")
    
    st.divider()
    
    # Configuration
    st.subheader("Configuration")
    speed_threshold = st.slider(
        "Superhuman Speed Threshold (req/s)",
        min_value=5.0,
        max_value=50.0,
        value=10.0,
        step=1.0
    )
    
    attack_intensity = st.slider(
        "Attack Intensity",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get('attack_intensity', 0.1),
        step=0.1,
        help="Controls the ratio of attack traffic. 0.0 = normal traffic only, 1.0 = attack traffic only"
    )
    
    # Store attack intensity in session state
    st.session_state.attack_intensity = attack_intensity
    
    # Trigger attack based on intensity
    if attack_intensity > 0.0:
        if not st.session_state.simulator.is_attacking:
            st.session_state.simulator.start_attack()
    else:
        if st.session_state.simulator.is_attacking:
            st.session_state.simulator.stop_attack()
    
    # Display attack status
    if st.session_state.simulator.is_attacking:
        st.info("🔴 **Attack Mode Active** - Generating GTG-1002 style attack traffic")
    else:
        st.info("🟢 **Normal Mode** - Generating normal traffic")
    
    st.divider()
    
    # Test Attack button
    test_attack_active = st.session_state.get('test_attack_active', False)
    test_attack_count = st.session_state.get('test_attack_count', 0)
    
    if test_attack_active:
        if test_attack_count >= 20:
            # Restore previous intensity
            prev_intensity = st.session_state.get('test_attack_prev_intensity', 0.1)
            st.session_state.attack_intensity = prev_intensity
            st.session_state.test_attack_active = False
            st.session_state.test_attack_count = 0
            if prev_intensity == 0.0:
                st.session_state.simulator.stop_attack()
            st.success("✅ Test attack completed! Generated 20 rapid requests. Check detections below.")
        else:
            st.info(f"🚀 Test attack in progress... ({test_attack_count}/20 requests)")
    else:
        if st.button("🚀 Test Attack", help="Generate 20 rapid attack requests for quick testing"):
            # Store previous intensity
            prev_intensity = st.session_state.get('attack_intensity', 0.1)
            st.session_state.test_attack_active = True
            st.session_state.test_attack_count = 0
            st.session_state.test_attack_prev_intensity = prev_intensity
            
            # Set to full attack mode
            st.session_state.attack_intensity = 1.0
            st.session_state.simulator.start_attack()
            st.success("Test attack started! Generating 20 rapid requests...")
            st.rerun()
    
    st.divider()
    
    # Reset button
    if st.button("🔄 Reset Detector"):
        st.session_state.detector.clear_history()
        st.session_state.detections = []
        st.session_state.simulator.stop_attack()
        st.session_state.request_count = 0
        st.session_state.last_threat_detected = None
        st.session_state.test_attack_active = False
        st.success("Detector reset! (Database records preserved)")
    
    # Database management
    st.divider()
    st.subheader("💾 Database")
    
    db_stats = st.session_state.db.get_statistics()
    st.caption(f"Total detections in DB: {db_stats['total_detections']}")
    st.caption(f"Malicious: {db_stats['malicious_count']} | Suspicious: {db_stats['suspicious_count']} | Normal: {db_stats['normal_count']}")
    
    # Vector DB status with detailed information
    if st.session_state.db:
        vector_status = getattr(st.session_state.db, 'vector_db_status', 'unknown')
        if st.session_state.db.vector_db:
            try:
                vector_stats = st.session_state.db.vector_db.get_stats()
                st.caption(f"🔍 Vector DB: {vector_stats['total_vectors']} vectors (Similarity search enabled)")
            except Exception as e:
                st.caption(f"⚠️ Vector DB: Error accessing stats ({str(e)[:30]})")
        else:
            if vector_status == "chromadb_not_installed":
                st.caption("⚠️ Vector DB: ChromaDB not installed (Optional: `pip install chromadb`)")
            elif vector_status.startswith("failed"):
                st.caption(f"⚠️ Vector DB: {vector_status}")
            else:
                st.caption("⚠️ Vector DB: Disabled")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Old (>7 days)", help="Remove detections older than 7 days"):
            deleted = st.session_state.db.clear_old_detections(days=7)
            st.success(f"Deleted {deleted} old detections")
            st.rerun()
    
    with col2:
        if st.button("🔄 Reload from DB", help="Reload recent detections from database"):
            recent_from_db = st.session_state.db.get_recent_detections(limit=100)
            st.session_state.detections = recent_from_db
            st.session_state.request_count = len(recent_from_db)
            st.success(f"Reloaded {len(recent_from_db)} detections from database")
            st.rerun()
    
    # Export button
    if st.session_state.detections:
        df = pd.DataFrame([d.to_dict() for d in st.session_state.detections])
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Export Detections",
            data=csv,
            file_name=f"detections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Main content area - Simulation loop (moved after charts for better visibility)
if st.session_state.running:
    # Get current attack intensity from session state
    attack_intensity = st.session_state.get('attack_intensity', 0.1)
    
    # Generate multiple requests per iteration to overcome single-threaded limitation
    # For attacks, generate batches to build up detection patterns faster
    if attack_intensity > 0.0:
        batch_size = 5  # Generate 5 requests per iteration for attacks
        sleep_time = 0.05  # Minimal sleep for attacks
    else:
        batch_size = 1  # One request at a time for normal traffic
        sleep_time = 1.0  # Normal speed for regular traffic
    
    # Process batch of requests
    try:
        # Use no_sleep=True for dashboard to control timing ourselves
        request_gen = st.session_state.simulator.generate_requests(attack_intensity=attack_intensity, no_sleep=True)
        
        for i in range(batch_size):
            request = next(request_gen)
            
            # Ensure timestamps are slightly spaced for speed detection
            # Add microsecond increments to simulate rapid requests
            if attack_intensity > 0.0 and i > 0:
                request.timestamp = datetime.now()  # Update timestamp for each request
            
            # Analyze request
            detection = st.session_state.detector.analyze_request(request)
            st.session_state.detections.append(detection)
            st.session_state.request_count += 1
            
            # Save to database
            try:
                st.session_state.db.save_detection(detection)
            except Exception as e:
                st.session_state.std_logger = st.session_state.get('std_logger') or __import__('logging').getLogger(__name__)
                st.session_state.std_logger.warning(f"Failed to save detection to database: {e}")
            
            # Track when threats are detected
            if detection.threat_level.value in ['suspicious', 'malicious']:
                st.session_state.last_threat_detected = datetime.now()
            
            # Handle test attack
            if st.session_state.get('test_attack_active', False):
                test_count = st.session_state.get('test_attack_count', 0)
                st.session_state.test_attack_count = test_count + 1
                # Stop after 20 requests for test attack
                if test_count >= 19:  # Already at 19, this makes it 20
                    break
        
        # Keep only recent detections
        if len(st.session_state.detections) > 1000:
            st.session_state.detections = st.session_state.detections[-1000:]
        
        # Update last update time for chart refresh tracking
        st.session_state.last_update = datetime.now()
        
        # Use slightly longer sleep to allow charts to render
        # Charts are rendered before this loop, so they'll be visible during simulation
        time.sleep(max(sleep_time, 0.3))  # Minimum 300ms to allow chart rendering
        st.rerun()
    except StopIteration:
        pass

# Visual feedback section
if st.session_state.running:
    # Request counter
    request_count = st.session_state.get('request_count', 0)
    st.caption(f"📊 **Requests Processed:** {request_count}")
    
    # Threat detection banner
    last_threat = st.session_state.get('last_threat_detected')
    if last_threat:
        time_since = (datetime.now() - last_threat).total_seconds()
        if time_since < 5:  # Show banner for 5 seconds after threat
            malicious_count = sum(1 for d in st.session_state.detections 
                                if d.threat_level.value == 'malicious')
            suspicious_count = sum(1 for d in st.session_state.detections 
                                 if d.threat_level.value == 'suspicious')
            
            if malicious_count > 0:
                st.error(f"🚨 **THREAT DETECTED!** {malicious_count} malicious threat(s) detected!")
            elif suspicious_count > 0:
                st.warning(f"⚠️ **Suspicious Activity Detected!** {suspicious_count} suspicious detection(s)")

# Metrics row with tooltips
st.markdown("#### Key Metrics")
col1, col2, col3, col4 = st.columns(4)

metrics = get_metrics_summary(st.session_state.detections)

# Add delta indicators for metrics
prev_metrics = st.session_state.get('prev_metrics', {})

with col1:
    delta_detections = metrics["total_detections"] - prev_metrics.get("total_detections", 0)
    st.metric(
        "Total Detections", 
        metrics["total_detections"], 
        delta=delta_detections if delta_detections > 0 else None,
        help="Total number of requests analyzed. Includes normal, suspicious, and malicious traffic."
    )

with col2:
    delta_malicious = metrics["malicious_count"] - prev_metrics.get("malicious_count", 0)
    st.metric(
        "Malicious Threats", 
        metrics["malicious_count"], 
        delta=delta_malicious if delta_malicious > 0 else None,
        delta_color="inverse",
        help="Number of confirmed malicious attacks detected (threat score 70-100). Requires immediate attention."
    )

with col3:
    delta_avg = metrics["avg_threat_score"] - prev_metrics.get("avg_threat_score", 0)
    st.metric(
        "Avg Threat Score", 
        f"{metrics['avg_threat_score']}/100",
        delta=f"{delta_avg:+.1f}" if abs(delta_avg) > 0.1 else None,
        help="Average threat score across all detections. Higher scores indicate more severe threats."
    )

with col4:
    delta_peak = metrics["peak_threat_score"] - prev_metrics.get("peak_threat_score", 0)
    st.metric(
        "Peak Threat Score", 
        f"{metrics['peak_threat_score']}/100",
        delta=delta_peak if delta_peak > 0 else None,
        delta_color="inverse",
        help="Highest threat score detected. Shows the most severe attack encountered."
    )

# Store current metrics for next comparison
st.session_state.prev_metrics = metrics.copy()

# Charts section - render BEFORE simulation loop so they're visible during simulation
st.divider()
st.subheader("📊 Visualizations")

# Add status indicator for charts with update info
if st.session_state.running:
    detection_count = len(st.session_state.detections)
    last_update = st.session_state.get('last_update', datetime.now())
    time_since_update = (datetime.now() - last_update).total_seconds()
    
    status_col1, status_col2 = st.columns([3, 1])
    with status_col1:
        st.info(f"🔄 **Live Mode**: Charts updating in real-time ({detection_count} detections processed)")
    with status_col2:
        if time_since_update < 1:
            st.caption("⚡ Updating...")
        else:
            st.caption(f"⏱️ {time_since_update:.1f}s ago")
else:
    if st.session_state.detections:
        detection_count = len(st.session_state.detections)
        st.success(f"✅ **Charts Ready**: Showing {detection_count} detection(s). Start simulation for live updates.")
    else:
        st.info("💡 **Tip**: Click '▶️ Start Simulation' to begin generating detections and see real-time visualizations.")

# Charts row
col1, col2 = st.columns(2)

with col1:
    col_title, col_help = st.columns([4, 1])
    with col_title:
        st.markdown("#### Threat Timeline")
    with col_help:
        st.markdown("""
        <div style="margin-top: 0.5rem;">
            <span title="Shows threat scores over time. Green = normal, Orange = suspicious, Red = malicious. Helps identify attack patterns and timing.">
                ℹ️
            </span>
        </div>
        """, unsafe_allow_html=True)
    with st.expander("ℹ️ What is Threat Timeline?", expanded=False):
        st.markdown("""
        **Threat Timeline** shows how threat scores change over time:
        - **Green dots**: Normal traffic (score 0-29)
        - **Orange dots**: Suspicious activity (score 30-69)
        - **Red dots**: Malicious attacks (score 70-100)
        
        Use this chart to identify attack patterns, timing, and escalation trends.
        """)
    if st.session_state.detections:
        timeline_chart = create_threat_timeline(st.session_state.detections, window_minutes=10)
        st.plotly_chart(
            timeline_chart,
            use_container_width=True,
            key="threat_timeline_chart"
        )
    else:
        st.info("No detections yet. Start simulation to see threat timeline.")

with col2:
    col_title, col_help = st.columns([4, 1])
    with col_title:
        st.markdown("#### Threat Level Gauge")
    with col_help:
        st.markdown("""
        <div style="margin-top: 0.5rem;">
            <span title="Current average threat level. Green = safe, Yellow = caution, Red = danger. Updates in real-time.">
                ℹ️
            </span>
        </div>
        """, unsafe_allow_html=True)
    with st.expander("ℹ️ What is Threat Level Gauge?", expanded=False):
        st.markdown("""
        **Threat Level Gauge** displays the current average threat score:
        - **Green zone (0-29)**: Low threat - normal traffic
        - **Yellow zone (30-69)**: Medium threat - suspicious activity detected
        - **Red zone (70-100)**: High threat - malicious attacks detected
        
        This gives you a quick visual indicator of overall system security status.
        """)
    if st.session_state.detections:
        current_score = metrics["avg_threat_score"] if st.session_state.detections else 0
        gauge_chart = create_threat_gauge(int(current_score))
        st.plotly_chart(
            gauge_chart,
            use_container_width=True,
            key="threat_gauge_chart"
        )
    else:
        st.info("No detections yet. Start simulation to see threat gauge.")

# Pattern distribution
col_title, col_help = st.columns([4, 1])
with col_title:
    st.markdown("#### Pattern Distribution")
with col_help:
    st.markdown("""
    <div style="margin-top: 0.5rem;">
        <span title="Shows breakdown of detected attack patterns. Helps understand what types of threats are most common.">
            ℹ️
        </span>
    </div>
    """, unsafe_allow_html=True)
with st.expander("ℹ️ What is Pattern Distribution?", expanded=False):
    st.markdown("""
    **Pattern Distribution** shows the breakdown of detected attack types:
    - **Superhuman Speed**: Requests too fast for humans (AI-driven)
    - **Systematic Enumeration**: Sequential endpoint discovery attempts
    - **Behavioral Anomaly**: Statistical deviations from normal patterns
    - **Normal**: Regular legitimate traffic
    
    Use this to understand which attack vectors are most prevalent.
    """)
if st.session_state.detections:
    pattern_chart = create_pattern_distribution(st.session_state.detections)
    st.plotly_chart(
        pattern_chart,
        use_container_width=True,
        key="pattern_distribution_chart"
    )
else:
    st.info("No detections yet. Start simulation to see pattern distribution.")

# Alerts and recent detections
col1, col2 = st.columns([1, 1])

with col1:
    col_title, col_help = st.columns([4, 1])
    with col_title:
        st.subheader("🚨 Recent Alerts")
    with col_help:
        st.markdown("""
        <div style="margin-top: 0.5rem;">
            <span title="Real-time security alerts for suspicious and malicious activity. Click buttons for detailed analysis.">
                ℹ️
            </span>
        </div>
        """, unsafe_allow_html=True)
    with st.expander("ℹ️ What are Recent Alerts?", expanded=False):
        st.markdown("""
        **Recent Alerts** show real-time security notifications:
        - **🔴 High Severity**: Malicious attacks requiring immediate attention
        - **🟡 Medium Severity**: Suspicious activity that should be investigated
        
        Each alert includes:
        - Threat type and details
        - Source IP address
        - Targeted endpoint
        - Timestamp
        
        Use "🤖 AI Insights" for detailed analysis or "🔍 Find Similar" to correlate attacks.
        """)
    alerts = create_alerts(st.session_state.detections, limit=10)
    
    if alerts:
        for alert in alerts:
            severity_color = get_alert_color(alert.severity)
            alert_class = f"alert-{alert.severity}"
            
            # Get AI explanation if available
            ai_explanation = ""
            if st.session_state.ai_enabled and st.session_state.detector:
                try:
                    ai_explanation = st.session_state.detector.get_threat_explanation(alert.detection)
                    if ai_explanation and ai_explanation != f"Threat detected: {alert.detection.pattern_type.value}":
                        ai_explanation = f"<br><em>AI Analysis: {ai_explanation[:150]}...</em>"
                    else:
                        ai_explanation = ""
                except:
                    pass
            
            st.markdown(f"""
            <div class="{alert_class}">
                <strong>{severity_color} {alert.severity.upper()}</strong> - {format_alert_time(alert.timestamp)}<br>
                <div class="alert-text">{alert.message}{ai_explanation}</div>
                <div class="alert-details">IP: {alert.detection.request.ip_address} | Endpoint: {alert.detection.request.endpoint}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add buttons for AI insights and similarity search
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.session_state.ai_enabled and st.session_state.ai_analyzer:
                    if st.button(f"🤖 AI Insights", key=f"ai_{alert.detection.timestamp}"):
                        st.session_state.selected_detection = alert.detection
            with col_btn2:
                if st.session_state.db and st.session_state.db.vector_db:
                    if st.button(f"🔍 Find Similar", key=f"similar_{alert.detection.timestamp}"):
                        st.session_state.selected_detection = alert.detection
                        st.session_state.show_similar = True
    else:
        st.info("No alerts yet. Start simulation to see detections.")

with col2:
    st.subheader("📊 Recent Detections")
    
    # Get recent detections from session state (most recent first)
    if st.session_state.detections:
        # Sort by timestamp descending (most recent first)
        recent = sorted(st.session_state.detections, key=lambda x: x.timestamp, reverse=True)[:20]
        
        detection_data = []
        for det in recent[:10]:  # Show top 10 most recent
            detection_data.append({
                "Time": det.timestamp.strftime("%H:%M:%S"),
                "Threat Score": det.threat_score,
                "Level": det.threat_level.value,
                "Pattern": det.pattern_type.value,
                "Endpoint": det.request.endpoint[:30] + "..." if len(det.request.endpoint) > 30 else det.request.endpoint,
                "IP": det.request.ip_address
            })
        
        df = pd.DataFrame(detection_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No detections yet. Start simulation to see detections.")

# Similar Attacks Panel (if detection selected and similarity search requested)
if (st.session_state.get('selected_detection') and 
    st.session_state.get('show_similar') and 
    st.session_state.db and 
    st.session_state.db.vector_db):
    
    st.divider()
    st.subheader("🔍 Similar Attacks")
    
    detection = st.session_state.selected_detection
    similar_detections = st.session_state.db.find_similar_detections(detection, limit=5)
    similar_panel = create_similar_attacks_panel(similar_detections, detection)
    
    if similar_panel["has_similar"]:
        st.info(f"Found {similar_panel['count']} similar attack(s) in history")
        
        for similar in similar_panel["similar"]:
            threat_emoji = {"normal": "🟢", "suspicious": "🟡", "malicious": "🔴"}
            emoji = threat_emoji.get(similar["threat_level"], "⚪")
            
            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; border-left: 3px solid #4CAF50; background-color: #f0f0f0;">
                <strong>{emoji} {similar['threat_level'].upper()}</strong> - {similar['time_ago']}<br>
                <strong>Pattern:</strong> {similar['pattern_type']}<br>
                <strong>Score:</strong> {similar['threat_score']}/100<br>
                <strong>Endpoint:</strong> {similar['endpoint']}<br>
                <strong>IP:</strong> {similar['ip_address']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No similar attacks found in history. This may be a new attack pattern.")
    
    if st.button("Close Similar Attacks"):
        st.session_state.show_similar = False
        st.rerun()

# Threat Clusters Panel
if st.session_state.db and st.session_state.db.vector_db:
    st.divider()
    with st.expander("📊 Threat Clusters (Similar Attack Patterns)", expanded=False):
        clusters = st.session_state.db.get_threat_clusters(limit=5)
        cluster_panel = create_threat_cluster_panel(clusters)
        
        if cluster_panel["has_clusters"]:
            st.info(f"Found {cluster_panel['count']} threat cluster(s)")
            
            for i, cluster in enumerate(cluster_panel["clusters"], 1):
                st.markdown(f"### Cluster {i} ({cluster['size']} attacks)")
                st.caption(f"Pattern: {cluster['pattern_type']} | Level: {cluster['threat_level']}")
                st.caption(f"Representative: {cluster['representative_endpoint']} from {cluster['representative_ip']}")
        else:
            st.info("No threat clusters found. Need more detections for clustering.")

# AI Insights Panel (if detection selected)
if st.session_state.selected_detection and st.session_state.ai_enabled and st.session_state.ai_analyzer:
    st.divider()
    st.subheader("🤖 AI Threat Analysis")
    
    detection = st.session_state.selected_detection
    
    # Threat explanation card
    explanation_card = create_threat_explanation_card(detection, st.session_state.ai_analyzer)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {explanation_card.get('title', 'Threat Analysis')}")
        st.info(explanation_card.get('explanation', 'No explanation available'))
        
        if explanation_card.get('intent'):
            st.caption(f"**Classified Intent:** {explanation_card.get('intent', 'unknown')} "
                      f"(Confidence: {explanation_card.get('intent_confidence', 0.0):.1%})")
        
        # Recommendations
        recommendations = explanation_card.get('recommendations', [])
        if recommendations:
            st.markdown("### Recommended Actions")
            for i, rec in enumerate(recommendations[:5], 1):
                st.markdown(f"{i}. {rec}")
    
    with col2:
        st.markdown("### Detection Details")
        st.json({
            "Pattern": detection.pattern_type.value,
            "Threat Score": detection.threat_score,
            "Level": detection.threat_level.value,
            "Endpoint": detection.request.endpoint,
            "IP": detection.request.ip_address,
            "AI Enhanced": explanation_card.get('ai_enhanced', False)
        })
        
        if explanation_card.get('model'):
            st.caption(f"Model: {explanation_card.get('model')}")
    
    # Attack scenario
    try:
        scenario = generate_attack_scenario_description(
            detection.pattern_type.value,
            detection.details,
            st.session_state.ai_analyzer
        )
        if scenario:
            with st.expander("📖 Attack Scenario"):
                st.write(scenario)
    except:
        pass
    
    if st.button("Close AI Analysis"):
        st.session_state.selected_detection = None
        st.rerun()

# AI Recommendations Panel
if st.session_state.ai_enabled and st.session_state.detections:
    malicious_detections = [d for d in st.session_state.detections if d.threat_level.value == "malicious"]
    if malicious_detections:
        st.divider()
        st.subheader("💡 AI Security Recommendations")
        
        recommendations = create_ai_recommendations_panel(malicious_detections[-5:], st.session_state.ai_analyzer)
        
        if recommendations:
            for rec in recommendations[:5]:
                priority_color = "🔴" if rec.get('priority') == 'high' else "🟡"
                st.markdown(f"{priority_color} **{rec.get('pattern', 'Unknown')}**: {rec.get('recommendation', '')}")

# Security Assistant Q&A (collapsible)
if st.session_state.ai_enabled and st.session_state.security_assistant:
    st.divider()
    with st.expander("💬 Ask Security Assistant"):
        question = st.text_input("Ask a question about threats, detection, or security:")
        if question:
            with st.spinner("AI is thinking..."):
                answer = st.session_state.security_assistant.answer_question(question)
                st.markdown(f"**Answer:**\n{answer.get('answer', 'Unable to generate answer.')}")
                if answer.get('sources'):
                    st.caption(f"Sources: {', '.join(answer.get('sources', []))}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>AI Pattern Detector - GTG-1002 Defense System | 
    Detecting autonomous AI-driven cyberattacks in real-time
    {" | 🤖 AI-Enhanced" if st.session_state.ai_enabled else ""}</small>
</div>
""", unsafe_allow_html=True)

