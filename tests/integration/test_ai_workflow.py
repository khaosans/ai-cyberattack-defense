"""
Integration tests for AI workflow
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
from ai_tools.ai_analysis.threat_analyzer import AIThreatAnalyzer
from ai_tools.ai_analysis.security_assistant import SecurityAssistant
from ai_tools.config import Config
from ai_tools.utils.models import Request, Detection, ThreatLevel, PatternType


@pytest.mark.integration
class TestAIWorkflowWithoutOllama:
    """Test AI workflow when Ollama is unavailable"""
    
    def test_enhanced_detector_workflow_no_ai(self):
        """Test enhanced detector workflow without AI"""
        config = Config()
        config.AI_ANALYSIS_ENABLED = False
        detector = EnhancedAIPatternDetector(config=config, enable_ai=False)
        
        # Create suspicious request
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
                # Should work without AI
                assert detection.threat_score >= 0
                break
    
    def test_threat_explanation_fallback(self):
        """Test threat explanation fallback"""
        config = Config()
        detector = EnhancedAIPatternDetector(config=config, enable_ai=False)
        
        request = Request(
            timestamp=datetime.now(),
            ip_address="10.0.0.1",
            endpoint="/api/admin/users",
            method="GET",
            user_agent="python-requests"
        )
        detection = detector.analyze_request(request)
        
        explanation = detector.get_threat_explanation(detection)
        assert isinstance(explanation, str)
        assert len(explanation) > 0
    
    def test_recommendations_fallback(self):
        """Test recommendations fallback"""
        config = Config()
        detector = EnhancedAIPatternDetector(config=config, enable_ai=False)
        
        request = Request(
            timestamp=datetime.now(),
            ip_address="10.0.0.1",
            endpoint="/api/admin/users",
            method="GET",
            user_agent="python-requests"
        )
        detection = detector.analyze_request(request)
        
        recommendations = detector.get_ai_recommendations(detection)
        assert isinstance(recommendations, list)


@pytest.mark.integration
class TestAIWorkflowWithMockOllama:
    """Test AI workflow with mocked Ollama"""
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_full_ai_analysis_workflow(self, mock_client_class):
        """Test full AI analysis workflow"""
        mock_client = Mock()
        mock_client.list.return_value = {"models": [{"name": "llama3"}]}
        mock_client.generate.return_value = {
            "response": "This is a reconnaissance attack pattern."
        }
        mock_client_class.return_value = mock_client
        
        config = Config()
        config.AI_ANALYSIS_ENABLED = True
        
        detector = EnhancedAIPatternDetector(config=config, enable_ai=True)
        
        # Create suspicious request
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
                # Should enhance with AI if available
                explanation = detector.get_threat_explanation(detection)
                assert isinstance(explanation, str)
                break
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_security_assistant_workflow(self, mock_client_class):
        """Test security assistant workflow"""
        mock_client = Mock()
        mock_client.list.return_value = {"models": [{"name": "llama3"}]}
        mock_client.generate.return_value = {
            "response": "Superhuman speed detection identifies requests occurring at rates impossible for human operators."
        }
        mock_client_class.return_value = mock_client
        
        config = Config()
        assistant = SecurityAssistant(config=config)
        
        # Test Q&A
        answer = assistant.answer_question("What is superhuman speed detection?")
        assert "answer" in answer
        assert isinstance(answer["answer"], str)
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_threat_analyzer_workflow(self, mock_client_class):
        """Test threat analyzer workflow"""
        mock_client = Mock()
        mock_client.list.return_value = {"models": [{"name": "llama3"}]}
        mock_client.generate.return_value = {
            "response": "This appears to be a systematic enumeration attack."
        }
        mock_client_class.return_value = mock_client
        
        config = Config()
        analyzer = AIThreatAnalyzer(config=config)
        
        # Create detection
        request = Request(
            timestamp=datetime.now(),
            ip_address="10.0.0.1",
            endpoint="/api/users/1",
            method="GET",
            user_agent="python-requests"
        )
        detection = Detection(
            timestamp=datetime.now(),
            request=request,
            threat_score=75,
            threat_level=ThreatLevel.MALICIOUS,
            pattern_type=PatternType.SYSTEMATIC_ENUMERATION,
            details={"sequence_length": 5}
        )
        
        # Analyze detection
        analysis = analyzer.analyze_detection(detection)
        assert isinstance(analysis, dict)
        # May have AI enhancement or fallback
        assert "explanation" in analysis or "ai_enhanced" in analysis


@pytest.mark.integration
class TestAIErrorHandling:
    """Test AI error handling in workflow"""
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_ai_error_handling(self, mock_client_class):
        """Test handling of AI errors"""
        mock_client = Mock()
        mock_client.list.side_effect = Exception("Connection failed")
        mock_client_class.return_value = mock_client
        
        config = Config()
        detector = EnhancedAIPatternDetector(config=config, enable_ai=True)
        
        # Should handle errors gracefully
        request = Request(
            timestamp=datetime.now(),
            ip_address="192.168.1.100",
            endpoint="/api/users/1",
            method="GET",
            user_agent="test"
        )
        
        # Should not raise exception
        detection = detector.analyze_request(request)
        assert detection is not None
        assert detection.threat_score >= 0

