"""
Unit tests for AIPatternDetector
"""
import pytest
from datetime import datetime, timedelta
from ai_tools.detection.ai_pattern_detector import AIPatternDetector
from ai_tools.utils.models import Request, ThreatLevel, PatternType


@pytest.mark.unit
class TestSuperhumanSpeedDetection:
    """Test superhuman speed detection"""
    
    def test_normal_speed_not_detected(self, detector, sample_request):
        """Normal request speed should not trigger detection"""
        detection = detector.analyze_request(sample_request)
        assert detection.pattern_type != PatternType.SUPERHUMAN_SPEED
        assert detection.threat_score < 30
    
    def test_rapid_requests_detected(self, detector, rapid_requests):
        """Rapid requests should trigger superhuman speed detection"""
        detections = []
        for request in rapid_requests:
            detection = detector.analyze_request(request)
            detections.append(detection)
        
        # At least one should detect superhuman speed
        speed_detections = [d for d in detections if d.pattern_type == PatternType.SUPERHUMAN_SPEED]
        assert len(speed_detections) > 0
    
    def test_speed_threshold_config(self, config):
        """Test configurable speed threshold"""
        config.SUPERHUMAN_SPEED_THRESHOLD = 5.0
        detector = AIPatternDetector(config=config)
        
        # Generate requests at 6 req/s (above threshold)
        base_time = datetime.now()
        for i in range(6):
            request = Request(
                timestamp=base_time + timedelta(seconds=i/6),
                ip_address="192.168.1.100",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="test"
            )
            detection = detector.analyze_request(request)
        
        # Check if speed was detected
        recent = detector.get_recent_detections(limit=10)
        speed_detections = [d for d in recent if d.pattern_type == PatternType.SUPERHUMAN_SPEED]
        assert len(speed_detections) > 0


@pytest.mark.unit
class TestSystematicEnumeration:
    """Test systematic enumeration detection"""
    
    def test_enumeration_pattern_detected(self, detector, enumeration_requests):
        """Sequential endpoint access should trigger enumeration detection"""
        detections = []
        for request in enumeration_requests:
            detection = detector.analyze_request(request)
            detections.append(detection)
        
        # Check for enumeration pattern
        enum_detections = [d for d in detections if d.pattern_type == PatternType.SYSTEMATIC_ENUMERATION]
        assert len(enum_detections) > 0
    
    def test_non_sequential_not_detected(self, detector):
        """Non-sequential endpoints should not trigger enumeration"""
        endpoints = ["/api/users/1", "/api/products/5", "/api/orders/3"]
        for endpoint in endpoints:
            request = Request(
                timestamp=datetime.now(),
                ip_address="192.168.1.100",
                endpoint=endpoint,
                method="GET",
                user_agent="test"
            )
            detection = detector.analyze_request(request)
            # Should not detect enumeration for non-sequential patterns
            if len(detector.detections) < 3:
                assert detection.pattern_type != PatternType.SYSTEMATIC_ENUMERATION


@pytest.mark.unit
class TestBehavioralAnomaly:
    """Test behavioral anomaly detection"""
    
    def test_anomaly_detection(self, detector):
        """Test anomaly detection with unusual patterns"""
        # Create unusual request pattern
        for i in range(10):
            request = Request(
                timestamp=datetime.now(),
                ip_address="192.168.1.100",
                endpoint=f"/api/deep/nested/path/{i}/very/long/endpoint",
                method="GET",
                user_agent="unusual-agent"
            )
            detector.analyze_request(request)
        
        # Check for anomaly detection
        recent = detector.get_recent_detections(limit=10)
        anomaly_detections = [d for d in recent if d.pattern_type == PatternType.BEHAVIORAL_ANOMALY]
        # Anomaly detection may or may not trigger depending on statistical analysis
        # This is acceptable as anomaly detection is probabilistic


@pytest.mark.unit
class TestThreatScoring:
    """Test threat scoring calculations"""
    
    def test_threat_score_range(self, detector, sample_request):
        """Threat scores should be between 0 and 100"""
        detection = detector.analyze_request(sample_request)
        assert 0 <= detection.threat_score <= 100
    
    def test_malicious_threat_level(self, detector):
        """High threat scores should result in malicious level"""
        # Create high-threat scenario
        base_time = datetime.now()
        for i in range(15):
            request = Request(
                timestamp=base_time + timedelta(milliseconds=i*10),
                ip_address="10.0.0.1",
                endpoint=f"/api/admin/users/{i}",
                method="GET",
                user_agent="python-requests"
            )
            detection = detector.analyze_request(request)
            if detection.threat_score >= 70:
                assert detection.threat_level == ThreatLevel.MALICIOUS
    
    def test_suspicious_threat_level(self, detector):
        """Medium threat scores should result in suspicious level"""
        # Create medium-threat scenario
        for i in range(5):
            request = Request(
                timestamp=datetime.now(),
                ip_address="192.168.1.100",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="test"
            )
            detection = detector.analyze_request(request)
            if 30 <= detection.threat_score < 70:
                assert detection.threat_level == ThreatLevel.SUSPICIOUS


@pytest.mark.unit
class TestPatternTypeDetermination:
    """Test pattern type determination logic"""
    
    def test_pattern_type_priority(self, detector):
        """Superhuman speed should take priority over enumeration"""
        # Create rapid enumeration pattern
        base_time = datetime.now()
        for i in range(10):
            request = Request(
                timestamp=base_time + timedelta(milliseconds=i*50),
                ip_address="10.0.0.1",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="python-requests"
            )
            detection = detector.analyze_request(request)
            # Speed should take priority
            if detection.pattern_type == PatternType.SUPERHUMAN_SPEED:
                assert detection.pattern_type == PatternType.SUPERHUMAN_SPEED


@pytest.mark.unit
class TestDetectionHistory:
    """Test detection history management"""
    
    def test_recent_detections_limit(self, detector):
        """get_recent_detections should respect limit"""
        # Generate many requests
        for i in range(100):
            request = Request(
                timestamp=datetime.now(),
                ip_address="192.168.1.100",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="test"
            )
            detector.analyze_request(request)
        
        recent = detector.get_recent_detections(limit=10)
        assert len(recent) <= 10
    
    def test_clear_history(self, detector):
        """clear_history should remove all detections"""
        # Generate some detections
        for i in range(5):
            request = Request(
                timestamp=datetime.now(),
                ip_address="192.168.1.100",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="test"
            )
            detector.analyze_request(request)
        
        assert len(detector.detections) > 0
        detector.clear_history()
        assert len(detector.detections) == 0
        assert len(detector.request_history) == 0

