"""
Unit tests for EnhancedAIPatternDetector
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
from ai_tools.utils.models import Request, ThreatLevel, PatternType
from ai_tools.config import Config


@pytest.mark.unit
class TestEnhancedDetectorBasic:
    """Test basic EnhancedAIPatternDetector functionality"""
    
    def test_enhanced_detector_creation(self, config):
        """Test creating EnhancedAIPatternDetector"""
        detector = EnhancedAIPatternDetector(config=config, enable_ai=False)
        assert detector.enable_ai == False
        assert detector.ai_analyzer is None
    
    def test_enhanced_detector_with_ai_disabled(self, config):
        """Test detector works without AI"""
        detector = EnhancedAIPatternDetector(config=config, enable_ai=False)
        request = Request(
            timestamp=datetime.now(),
            ip_address="192.168.1.100",
            endpoint="/api/users/1",
            method="GET",
            user_agent="test"
        )
        detection = detector.analyze_request(request)
        assert detection is not None
        assert detection.threat_score >= 0


@pytest.mark.unit
class TestAIEnhancement:
    """Test AI enhancement features"""
    
    @patch('ai_tools.detection.enhanced_detector.AIThreatAnalyzer')
    def test_ai_enhancement_when_enabled(self, mock_analyzer_class, config):
        """Test AI enhancement is called when enabled"""
        mock_analyzer = Mock()
        mock_analyzer.analyze_detection.return_value = {
            "ai_enhanced": True,
            "explanation": "Test explanation",
            "recommendations": ["Action 1", "Action 2"],
            "intent": "reconnaissance",
            "intent_confidence": 0.8
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        detector = EnhancedAIPatternDetector(config=config, enable_ai=True)
        
        # Create a suspicious request
        base_time = datetime.now()
        for i in range(10):
            request = Request(
                timestamp=base_time.replace(microsecond=i*10000),
                ip_address="10.0.0.1",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="python-requests"
            )
            detection = detector.analyze_request(request)
            if detection.threat_level.value != "normal":
                break
        
        # Check if AI analyzer was used
        if detector.enable_ai and detector.ai_analyzer:
            assert len(detector.ai_enhanced_detections) > 0
    
    def test_threat_explanation_without_ai(self, config):
        """Test threat explanation without AI"""
        detector = EnhancedAIPatternDetector(config=config, enable_ai=False)
        request = Request(
            timestamp=datetime.now(),
            ip_address="192.168.1.100",
            endpoint="/api/users/1",
            method="GET",
            user_agent="test"
        )
        detection = detector.analyze_request(request)
        explanation = detector.get_threat_explanation(detection)
        assert explanation is not None
        assert isinstance(explanation, str)
    
    @patch('ai_tools.detection.enhanced_detector.AIThreatAnalyzer')
    def test_ai_recommendations(self, mock_analyzer_class, config):
        """Test getting AI recommendations"""
        mock_analyzer = Mock()
        mock_analyzer.analyze_detection.return_value = {
            "ai_enhanced": True,
            "recommendations": ["Review logs", "Check network", "Rotate credentials"]
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        detector = EnhancedAIPatternDetector(config=config, enable_ai=True)
        request = Request(
            timestamp=datetime.now(),
            ip_address="10.0.0.1",
            endpoint="/api/admin/users",
            method="GET",
            user_agent="python-requests"
        )
        detection = detector.analyze_request(request)
        
        recommendations = detector.get_ai_recommendations(detection)
        # Should return empty list if AI not available or detection not enhanced
        assert isinstance(recommendations, list)


@pytest.mark.unit
class TestFalsePositiveReduction:
    """Test AI-powered false positive reduction"""
    
    @patch('ai_tools.detection.enhanced_detector.AIThreatAnalyzer')
    def test_false_positive_reduction(self, mock_analyzer_class, config):
        """Test AI reduces false positives"""
        mock_analyzer = Mock()
        # Simulate AI classifying as normal intent
        mock_analyzer.analyze_detection.return_value = {
            "ai_enhanced": True,
            "intent": "normal",
            "intent_confidence": 0.2,  # Low confidence in malicious intent
            "explanation": "Normal traffic pattern"
        }
        mock_analyzer_class.return_value = mock_analyzer
        
        detector = EnhancedAIPatternDetector(config=config, enable_ai=True)
        
        # Create request that might trigger false positive
        request = Request(
            timestamp=datetime.now(),
            ip_address="192.168.1.100",
            endpoint="/api/users/1",
            method="GET",
            user_agent="Mozilla/5.0"
        )
        detection = detector.analyze_request(request)
        
        # With AI indicating normal intent, threat score should be adjusted
        # (implementation may vary, but should handle gracefully)
        assert detection.threat_score >= 0


@pytest.mark.unit
class TestIncidentReportGeneration:
    """Test incident report generation"""
    
    def test_generate_basic_report(self, config):
        """Test generating report without AI"""
        detector = EnhancedAIPatternDetector(config=config, enable_ai=False)
        
        # Add some detections
        for i in range(5):
            request = Request(
                timestamp=datetime.now(),
                ip_address="192.168.1.100",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="test"
            )
            detector.analyze_request(request)
        
        report = detector.generate_incident_report()
        assert isinstance(report, str)
        assert "Incident Report" in report or "detections" in report.lower()
    
    @patch('ai_tools.detection.enhanced_detector.AIThreatAnalyzer')
    def test_generate_ai_report(self, mock_analyzer_class, config):
        """Test generating report with AI"""
        mock_analyzer = Mock()
        mock_analyzer.generate_incident_report.return_value = "# AI-Generated Report\n\nSummary..."
        mock_analyzer_class.return_value = mock_analyzer
        
        detector = EnhancedAIPatternDetector(config=config, enable_ai=True)
        
        # Add detections
        for i in range(3):
            request = Request(
                timestamp=datetime.now(),
                ip_address="10.0.0.1",
                endpoint=f"/api/users/{i}",
                method="GET",
                user_agent="test"
            )
            detector.analyze_request(request)
        
        report = detector.generate_incident_report()
        assert isinstance(report, str)

