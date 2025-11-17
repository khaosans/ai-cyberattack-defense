"""
Unit tests for data models
"""
import pytest
from datetime import datetime
from ai_tools.utils.models import Request, Detection, ThreatLevel, PatternType, Alert


class TestRequest:
    """Test Request model"""
    
    def test_request_creation(self):
        """Test creating a Request object"""
        request = Request(
            timestamp=datetime.now(),
            ip_address="192.168.1.100",
            endpoint="/api/users/1",
            method="GET",
            user_agent="Mozilla/5.0"
        )
        assert request.ip_address == "192.168.1.100"
        assert request.endpoint == "/api/users/1"
        assert request.method == "GET"
    
    def test_request_to_dict(self):
        """Test Request serialization"""
        request = Request(
            timestamp=datetime(2025, 1, 1, 12, 0, 0),
            ip_address="192.168.1.100",
            endpoint="/api/users/1",
            method="GET",
            user_agent="Mozilla/5.0",
            parameters={"id": 1}
        )
        data = request.to_dict()
        assert data["ip_address"] == "192.168.1.100"
        assert data["endpoint"] == "/api/users/1"
        assert data["parameters"] == {"id": 1}
        assert "timestamp" in data


class TestDetection:
    """Test Detection model"""
    
    def test_detection_creation(self, sample_request):
        """Test creating a Detection object"""
        detection = Detection(
            timestamp=datetime.now(),
            request=sample_request,
            threat_score=75,
            threat_level=ThreatLevel.MALICIOUS,
            pattern_type=PatternType.SUPERHUMAN_SPEED,
            details={"requests_per_second": 15.0}
        )
        assert detection.threat_score == 75
        assert detection.threat_level == ThreatLevel.MALICIOUS
        assert detection.pattern_type == PatternType.SUPERHUMAN_SPEED
    
    def test_detection_to_dict(self, sample_request):
        """Test Detection serialization"""
        detection = Detection(
            timestamp=datetime(2025, 1, 1, 12, 0, 0),
            request=sample_request,
            threat_score=50,
            threat_level=ThreatLevel.SUSPICIOUS,
            pattern_type=PatternType.SYSTEMATIC_ENUMERATION,
            details={"sequence_length": 5}
        )
        data = detection.to_dict()
        assert data["threat_score"] == 50
        assert data["threat_level"] == "suspicious"
        assert data["pattern_type"] == "systematic_enumeration"
        assert "request" in data


class TestEnums:
    """Test enumeration types"""
    
    def test_threat_level_enum(self):
        """Test ThreatLevel enum values"""
        assert ThreatLevel.NORMAL.value == "normal"
        assert ThreatLevel.SUSPICIOUS.value == "suspicious"
        assert ThreatLevel.MALICIOUS.value == "malicious"
    
    def test_pattern_type_enum(self):
        """Test PatternType enum values"""
        assert PatternType.NORMAL.value == "normal"
        assert PatternType.SUPERHUMAN_SPEED.value == "superhuman_speed"
        assert PatternType.SYSTEMATIC_ENUMERATION.value == "systematic_enumeration"
        assert PatternType.BEHAVIORAL_ANOMALY.value == "behavioral_anomaly"


class TestAlert:
    """Test Alert model"""
    
    def test_alert_creation(self, sample_request):
        """Test creating an Alert object"""
        detection = Detection(
            timestamp=datetime.now(),
            request=sample_request,
            threat_score=80,
            threat_level=ThreatLevel.MALICIOUS,
            pattern_type=PatternType.SUPERHUMAN_SPEED,
            details={}
        )
        alert = Alert(
            timestamp=datetime.now(),
            severity="high",
            message="Malicious activity detected",
            detection=detection
        )
        assert alert.severity == "high"
        assert alert.message == "Malicious activity detected"
        assert alert.detection == detection
    
    def test_alert_to_dict(self, sample_request):
        """Test Alert serialization"""
        detection = Detection(
            timestamp=datetime.now(),
            request=sample_request,
            threat_score=60,
            threat_level=ThreatLevel.SUSPICIOUS,
            pattern_type=PatternType.BEHAVIORAL_ANOMALY,
            details={}
        )
        alert = Alert(
            timestamp=datetime(2025, 1, 1, 12, 0, 0),
            severity="medium",
            message="Suspicious pattern detected",
            detection=detection
        )
        data = alert.to_dict()
        assert data["severity"] == "medium"
        assert data["message"] == "Suspicious pattern detected"
        assert "detection" in data

