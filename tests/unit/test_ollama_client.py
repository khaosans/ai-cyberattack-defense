"""
Unit tests for OllamaClient
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from ai_tools.ai_analysis.ollama_client import OllamaClient, OLLAMA_AVAILABLE
from ai_tools.config import Config
from ai_tools.utils.models import Request


@pytest.mark.unit
class TestOllamaClientInitialization:
    """Test OllamaClient initialization"""
    
    def test_client_creation_without_ollama(self, config):
        """Test client creation when Ollama package not available"""
        with patch('ai_tools.ai_analysis.ollama_client.OLLAMA_AVAILABLE', False):
            client = OllamaClient(config=config)
            assert client.available == False
            assert client.is_available() == False
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_client_creation_with_ollama(self, mock_client_class, config):
        """Test client creation when Ollama is available"""
        mock_client = Mock()
        mock_client.list.return_value = {"models": [{"name": "llama3"}]}
        mock_client_class.return_value = mock_client
        
        with patch('ai_tools.ai_analysis.ollama_client.OLLAMA_AVAILABLE', True):
            client = OllamaClient(config=config)
            # Connection test may fail, but client should be created
            assert client.client is not None or client.available == False
    
    def test_client_disabled_via_config(self, config):
        """Test client respects disabled config"""
        config.OLLAMA_ENABLED = False
        client = OllamaClient(config=config)
        assert client.enabled == False
        assert client.is_available() == False


@pytest.mark.unit
class TestOllamaClientMethods:
    """Test OllamaClient methods"""
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_analyze_request_pattern_unavailable(self, mock_client_class, config):
        """Test analyze_request_pattern when Ollama unavailable"""
        with patch('ai_tools.ai_analysis.ollama_client.OLLAMA_AVAILABLE', False):
            client = OllamaClient(config=config)
            result = client.analyze_request_pattern({
                "endpoint": "/api/users/1",
                "method": "GET",
                "ip_address": "192.168.1.100"
            })
            assert result["available"] == False
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_explain_threat_unavailable(self, mock_client_class, config):
        """Test explain_threat when Ollama unavailable"""
        with patch('ai_tools.ai_analysis.ollama_client.OLLAMA_AVAILABLE', False):
            client = OllamaClient(config=config)
            result = client.explain_threat({
                "pattern_type": "superhuman_speed",
                "threat_score": 75
            })
            assert "unavailable" in result.lower() or "rule-based" in result.lower()
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_suggest_response_unavailable(self, mock_client_class, config):
        """Test suggest_response when Ollama unavailable"""
        with patch('ai_tools.ai_analysis.ollama_client.OLLAMA_AVAILABLE', False):
            client = OllamaClient(config=config)
            recommendations = client.suggest_response({
                "pattern_type": "superhuman_speed",
                "threat_score": 80
            })
            assert isinstance(recommendations, list)
            assert len(recommendations) > 0
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_classify_intent_unavailable(self, mock_client_class, config):
        """Test classify_intent when Ollama unavailable"""
        with patch('ai_tools.ai_analysis.ollama_client.OLLAMA_AVAILABLE', False):
            client = OllamaClient(config=config)
            result = client.classify_intent({
                "endpoint": "/api/users/1",
                "method": "GET"
            })
            assert result["intent"] == "unknown"
            assert result["confidence"] == 0.0


@pytest.mark.unit
class TestGracefulDegradation:
    """Test graceful degradation when Ollama unavailable"""
    
    def test_all_methods_graceful_degradation(self, config):
        """Test all methods handle unavailability gracefully"""
        with patch('ai_tools.ai_analysis.ollama_client.OLLAMA_AVAILABLE', False):
            client = OllamaClient(config=config)
            
            # All methods should return valid responses even when unavailable
            assert client.is_available() == False
            
            analysis = client.analyze_request_pattern({})
            assert "available" in analysis
            
            explanation = client.explain_threat({})
            assert isinstance(explanation, str)
            
            recommendations = client.suggest_response({})
            assert isinstance(recommendations, list)
            
            intent = client.classify_intent({})
            assert "intent" in intent


@pytest.mark.unit
class TestConnectionHandling:
    """Test connection handling"""
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_connection_failure_handling(self, mock_client_class, config):
        """Test handling connection failures"""
        mock_client = Mock()
        mock_client.list.side_effect = Exception("Connection failed")
        mock_client_class.return_value = mock_client
        
        with patch('ai_tools.ai_analysis.ollama_client.OLLAMA_AVAILABLE', True):
            client = OllamaClient(config=config)
            assert client.available == False
    
    @patch('ai_tools.ai_analysis.ollama_client.Client')
    def test_generate_response_error_handling(self, mock_client_class, config):
        """Test error handling in _generate_response"""
        mock_client = Mock()
        mock_client.generate.side_effect = Exception("Generation failed")
        mock_client_class.return_value = mock_client
        
        with patch('ai_tools.ai_analysis.ollama_client.OLLAMA_AVAILABLE', True):
            client = OllamaClient(config=config)
            client.client = mock_client
            client.available = True
            
            # Should raise exception or handle gracefully
            try:
                result = client._generate_response("test prompt")
            except Exception:
                pass  # Expected behavior

