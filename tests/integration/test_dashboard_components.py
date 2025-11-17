"""
Integration tests for dashboard components
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ai_tools.detection.ai_pattern_detector import AIPatternDetector
from ai_tools.utils.models import Request, Detection, ThreatLevel, PatternType
from datetime import datetime, timedelta
from dashboard.components.threat_chart import create_threat_timeline, create_pattern_distribution, create_threat_gauge
from dashboard.components.alert_feed import create_alerts, get_alert_color, format_alert_time
from dashboard.components.metrics_panel import get_metrics_summary


@pytest.mark.integration
class TestThreatChartComponents:
    """Test threat chart components"""
    
    def test_create_threat_timeline(self):
        """Test creating threat timeline chart"""
        detections = []
        base_time = datetime.now()
        
        for i in range(10):
            request = Request(
                timestamp=base_time + timedelta(minutes=i),
                ip_address="192.168.1.100",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="test"
            )
            detection = Detection(
                timestamp=base_time + timedelta(minutes=i),
                request=request,
                threat_score=i * 10,
                threat_level=ThreatLevel.NORMAL if i < 3 else ThreatLevel.SUSPICIOUS,
                pattern_type=PatternType.NORMAL,
                details={}
            )
            detections.append(detection)
        
        chart = create_threat_timeline(detections, window_minutes=60)
        assert chart is not None
    
    def test_create_pattern_distribution(self):
        """Test creating pattern distribution chart"""
        detections = []
        base_time = datetime.now()
        
        patterns = [
            PatternType.NORMAL,
            PatternType.SUPERHUMAN_SPEED,
            PatternType.SYSTEMATIC_ENUMERATION,
            PatternType.BEHAVIORAL_ANOMALY
        ]
        
        for i, pattern in enumerate(patterns):
            request = Request(
                timestamp=base_time + timedelta(minutes=i),
                ip_address="192.168.1.100",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="test"
            )
            detection = Detection(
                timestamp=base_time + timedelta(minutes=i),
                request=request,
                threat_score=50,
                threat_level=ThreatLevel.SUSPICIOUS,
                pattern_type=pattern,
                details={}
            )
            detections.append(detection)
        
        chart = create_pattern_distribution(detections)
        assert chart is not None
    
    def test_create_threat_gauge(self):
        """Test creating threat gauge"""
        chart = create_threat_gauge(75)
        assert chart is not None
        
        chart_low = create_threat_gauge(20)
        assert chart_low is not None
        
        chart_high = create_threat_gauge(90)
        assert chart_high is not None


@pytest.mark.integration
class TestAlertFeedComponents:
    """Test alert feed components"""
    
    def test_create_alerts(self):
        """Test creating alerts from detections"""
        detections = []
        base_time = datetime.now()
        
        for i in range(5):
            request = Request(
                timestamp=base_time + timedelta(minutes=i),
                ip_address="10.0.0.1",
                endpoint=f"/api/admin/{i}",
                method="GET",
                user_agent="python-requests"
            )
            detection = Detection(
                timestamp=base_time + timedelta(minutes=i),
                request=request,
                threat_score=60 + i * 5,
                threat_level=ThreatLevel.SUSPICIOUS if i < 3 else ThreatLevel.MALICIOUS,
                pattern_type=PatternType.SUPERHUMAN_SPEED,
                details={}
            )
            detections.append(detection)
        
        alerts = create_alerts(detections, limit=10)
        assert len(alerts) <= 10
        assert len(alerts) > 0
    
    def test_get_alert_color(self):
        """Test alert color mapping"""
        assert get_alert_color("malicious") is not None
        assert get_alert_color("suspicious") is not None
        assert get_alert_color("normal") is not None
    
    def test_format_alert_time(self):
        """Test alert time formatting"""
        test_time = datetime.now()
        formatted = format_alert_time(test_time)
        assert isinstance(formatted, str)
        assert len(formatted) > 0


@pytest.mark.integration
class TestMetricsPanel:
    """Test metrics panel components"""
    
    def test_get_metrics_summary(self):
        """Test getting metrics summary"""
        detections = []
        base_time = datetime.now()
        
        for i in range(10):
            request = Request(
                timestamp=base_time + timedelta(minutes=i),
                ip_address="192.168.1.100",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="test"
            )
            detection = Detection(
                timestamp=base_time + timedelta(minutes=i),
                request=request,
                threat_score=i * 10,
                threat_level=ThreatLevel.NORMAL if i < 3 else ThreatLevel.SUSPICIOUS,
                pattern_type=PatternType.NORMAL,
                details={}
            )
            detections.append(detection)
        
        metrics = get_metrics_summary(detections)
        assert "total_detections" in metrics
        assert "malicious_count" in metrics
        assert "avg_threat_score" in metrics
        assert metrics["total_detections"] == 10
    
    def test_metrics_with_empty_detections(self):
        """Test metrics with empty detection list"""
        metrics = get_metrics_summary([])
        assert metrics["total_detections"] == 0
        assert metrics["malicious_count"] == 0
        assert metrics["avg_threat_score"] == 0

