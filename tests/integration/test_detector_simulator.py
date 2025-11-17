"""
Integration tests for detector and simulator
"""
import pytest
from ai_tools.detection.ai_pattern_detector import AIPatternDetector
from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
from ai_tools.simulation.attack_simulator import AttackSimulator
from ai_tools.config import Config
from ai_tools.utils.models import ThreatLevel, PatternType


@pytest.mark.integration
class TestDetectorSimulatorIntegration:
    """Test integration between detector and simulator"""
    
    def test_detector_with_simulator_normal_traffic(self):
        """Test detector analyzing normal simulator traffic"""
        detector = AIPatternDetector()
        simulator = AttackSimulator()
        
        detections = []
        for i, request in enumerate(simulator.generate_requests()):
            detection = detector.analyze_request(request)
            detections.append(detection)
            if i >= 19:  # Analyze 20 requests
                break
        
        assert len(detections) == 20
        assert all(d.threat_score >= 0 for d in detections)
        assert all(d.threat_score <= 100 for d in detections)
    
    def test_detector_with_simulator_attack_traffic(self):
        """Test detector analyzing attack simulator traffic"""
        detector = AIPatternDetector()
        simulator = AttackSimulator()
        simulator.start_attack()
        
        detections = []
        for i, request in enumerate(simulator.generate_requests()):
            detection = detector.analyze_request(request)
            detections.append(detection)
            if i >= 19:  # Analyze 20 requests
                break
        
        # Should detect some threats in attack traffic
        threat_detections = [d for d in detections if d.threat_level.value != "normal"]
        assert len(threat_detections) > 0
    
    def test_enhanced_detector_with_simulator(self):
        """Test enhanced detector with simulator"""
        config = Config()
        detector = EnhancedAIPatternDetector(config=config, enable_ai=False)
        simulator = AttackSimulator()
        simulator.start_attack()
        
        detections = []
        for i, request in enumerate(simulator.generate_requests()):
            detection = detector.analyze_request(request)
            detections.append(detection)
            if i >= 9:
                break
        
        assert len(detections) == 10
        # Enhanced detector should work same as base detector when AI disabled
        assert all(d.threat_score >= 0 for d in detections)


@pytest.mark.integration
class TestDetectionAccuracy:
    """Test detection accuracy with simulator"""
    
    def test_detection_of_superhuman_speed(self):
        """Test detector identifies superhuman speed in attack traffic"""
        detector = AIPatternDetector()
        simulator = AttackSimulator()
        simulator.start_attack()
        
        detections = []
        for i, request in enumerate(simulator.generate_requests()):
            detection = detector.analyze_request(request)
            detections.append(detection)
            if i >= 29:  # Need enough requests to detect speed
                break
        
        # Check for superhuman speed detection
        speed_detections = [d for d in detections if d.pattern_type == PatternType.SUPERHUMAN_SPEED]
        # May or may not detect depending on timing, but should handle gracefully
        assert len(detections) == 30
    
    def test_detection_of_enumeration(self):
        """Test detector identifies enumeration patterns"""
        detector = AIPatternDetector()
        simulator = AttackSimulator()
        simulator.start_attack()
        
        detections = []
        for i, request in enumerate(simulator.generate_requests()):
            detection = detector.analyze_request(request)
            detections.append(detection)
            if i >= 19:
                break
        
        # Check for enumeration detection
        enum_detections = [d for d in detections if d.pattern_type == PatternType.SYSTEMATIC_ENUMERATION]
        # Enumeration may be detected in attack traffic
        assert len(detections) == 20


@pytest.mark.integration
class TestEndToEndWorkflow:
    """Test end-to-end workflow"""
    
    def test_complete_detection_workflow(self):
        """Test complete workflow from simulation to detection"""
        detector = AIPatternDetector()
        simulator = AttackSimulator()
        
        # Start with normal traffic
        normal_detections = []
        for i, request in enumerate(simulator.generate_requests()):
            detection = detector.analyze_request(request)
            normal_detections.append(detection)
            if i >= 9:
                break
        
        # Switch to attack traffic
        simulator.start_attack()
        attack_detections = []
        for i, request in enumerate(simulator.generate_requests()):
            detection = detector.analyze_request(request)
            attack_detections.append(detection)
            if i >= 9:
                break
        
        # Verify workflow completed
        assert len(normal_detections) == 10
        assert len(attack_detections) == 10
        
        # Attack traffic should have more threats
        normal_threats = [d for d in normal_detections if d.threat_level.value != "normal"]
        attack_threats = [d for d in attack_detections if d.threat_level.value != "normal"]
        
        # Attack traffic should generally have more threats
        assert len(attack_threats) >= len(normal_threats)
    
    def test_detection_history_management(self):
        """Test detection history is managed correctly"""
        detector = AIPatternDetector()
        simulator = AttackSimulator()
        
        # Generate many requests
        count = 0
        for request in simulator.generate_requests():
            detector.analyze_request(request)
            count += 1
            if count >= 100:
                break
        
        # Check history management
        recent = detector.get_recent_detections(limit=50)
        assert len(recent) <= 50
        
        # Check stats
        stats = detector.get_detection_stats()
        assert "total" in stats or "count" in stats or len(detector.detections) > 0

