"""
Ollama Client - Wrapper for local Ollama LLM integration
"""
import json
import time
from typing import Optional, Dict, Any, List
from functools import lru_cache
import logging

try:
    from ollama import Client
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    Client = None

from ..config import Config


class OllamaClient:
    """
    Wrapper for Ollama API providing local LLM inference capabilities
    
    Features:
    - Connection management to local Ollama server
    - Model selection and management
    - Request/response handling with error handling
    - Caching for performance
    - Graceful fallback if Ollama unavailable
    """
    
    def __init__(self, host: Optional[str] = None, model: Optional[str] = None, config: Optional[Config] = None):
        """
        Initialize Ollama client
        
        Args:
            host: Ollama server URL (default: http://localhost:11434)
            model: Model name to use (default: llama3)
            config: Configuration object
        """
        self.config = config or Config()
        self.host = host or getattr(self.config, 'OLLAMA_HOST', 'http://localhost:11434')
        self.model = model or getattr(self.config, 'OLLAMA_MODEL', 'llama3')
        self.enabled = getattr(self.config, 'OLLAMA_ENABLED', True)
        self.cache_enabled = getattr(self.config, 'AI_CACHE_ENABLED', True)
        
        self.client = None
        self.available = False
        self.logger = logging.getLogger(__name__)
        
        if OLLAMA_AVAILABLE and self.enabled:
            try:
                self.client = Client(host=self.host)
                # Test connection
                self._test_connection()
            except Exception as e:
                self.logger.warning(f"Ollama not available: {e}")
                self.available = False
        else:
            if not OLLAMA_AVAILABLE:
                self.logger.warning("Ollama package not installed. Install with: pip install ollama")
            self.available = False
    
    def _test_connection(self) -> bool:
        """Test connection to Ollama server"""
        try:
            if self.client:
                # Simple test - list models
                response = self.client.list()
                
                # Handle ListResponse object (has .models attribute)
                if hasattr(response, 'models'):
                    models_list = response.models
                # Handle dict response
                elif isinstance(response, dict):
                    models_list = response.get('models', [])
                # Handle list response
                elif isinstance(response, list):
                    models_list = response
                else:
                    models_list = []
                
                # Extract model names safely
                available_models = []
                for m in models_list:
                    # Handle Model objects (has .model attribute)
                    if hasattr(m, 'model'):
                        available_models.append(m.model)
                    # Handle dict with 'name' or 'model' key
                    elif isinstance(m, dict):
                        model_name = m.get('name') or m.get('model')
                        if model_name:
                            available_models.append(model_name)
                    # Handle string
                    elif isinstance(m, str):
                        available_models.append(m)
                
                if available_models:
                    self.available = True
                    self.logger.info(f"Ollama connected successfully. Available models: {available_models}")
                    
                    # Check if configured model is available, if not use first available
                    if self.model not in available_models:
                        original_model = self.model
                        self.model = available_models[0]
                        self.logger.info(f"Model '{original_model}' not found, using '{available_models[0]}' instead")
                    
                    return True
                else:
                    self.logger.warning("Ollama connected but no models found")
                    self.available = False
                    return False
        except Exception as e:
            self.logger.warning(f"Ollama connection test failed: {e}")
            self.available = False
            return False
        return False
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        return self.available and self.enabled
    
    def analyze_request_pattern(self, request_data: Dict[str, Any], context: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Use LLM to analyze request patterns for threats
        
        Args:
            request_data: Request information (endpoint, method, IP, etc.)
            context: Additional context (recent requests, patterns)
            
        Returns:
            Dictionary with AI analysis results
        """
        if not self.is_available():
            return {"available": False, "analysis": None}
        
        prompt = self._build_analysis_prompt(request_data, context)
        
        try:
            response = self._generate_response(prompt)
            return {
                "available": True,
                "analysis": response,
                "model": self.model,
                "confidence": self._extract_confidence(response)
            }
        except Exception as e:
            self.logger.error(f"AI analysis failed: {e}")
            return {"available": False, "error": str(e)}
    
    def explain_threat(self, detection_data: Dict[str, Any]) -> str:
        """
        Generate natural language explanation of threat
        
        Args:
            detection_data: Detection information (pattern type, score, details)
            
        Returns:
            Natural language explanation
        """
        if not self.is_available():
            return "AI analysis unavailable. Using rule-based detection."
        
        prompt = f"""You are a cybersecurity expert. Explain this threat detection in clear, concise language.

Threat Detection:
- Pattern Type: {detection_data.get('pattern_type', 'unknown')}
- Threat Score: {detection_data.get('threat_score', 0)}/100
- Details: {json.dumps(detection_data.get('details', {}), indent=2)}

Provide a 2-3 sentence explanation of:
1. What this threat is
2. Why it's suspicious
3. What it might indicate

Keep it technical but accessible:"""
        
        try:
            response = self._generate_response(prompt)
            return response.get('response', 'Unable to generate explanation.')
        except Exception as e:
            self.logger.error(f"Threat explanation failed: {e}")
            return f"Threat detected: {detection_data.get('pattern_type', 'unknown pattern')}"
    
    def suggest_response(self, detection_data: Dict[str, Any]) -> List[str]:
        """
        Generate AI-powered response recommendations
        
        Args:
            detection_data: Detection information
            
        Returns:
            List of recommended actions
        """
        if not self.is_available():
            return [
                "Review detection logs",
                "Check network traffic",
                "Verify endpoint security"
            ]
        
        prompt = f"""You are a cybersecurity incident responder. Based on this threat detection, recommend specific security actions.

Threat Detection:
- Pattern: {detection_data.get('pattern_type', 'unknown')}
- Score: {detection_data.get('threat_score', 0)}/100
- Endpoint: {detection_data.get('endpoint', 'unknown')}
- IP: {detection_data.get('ip_address', 'unknown')}

Provide 3-5 specific, actionable security recommendations. Format as a numbered list:"""
        
        try:
            response = self._generate_response(prompt)
            text = response.get('response', '')
            # Extract numbered list items
            recommendations = [line.strip() for line in text.split('\n') if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-'))]
            return recommendations[:5] if recommendations else ["Review detection", "Investigate endpoint", "Check network logs"]
        except Exception as e:
            self.logger.error(f"Response suggestion failed: {e}")
            return ["Review detection logs", "Investigate endpoint"]
    
    def classify_intent(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify request intent using AI
        
        Args:
            request_data: Request information
            
        Returns:
            Classification results (intent, confidence, reasoning)
        """
        if not self.is_available():
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "reasoning": "AI analysis unavailable"
            }
        
        prompt = f"""Analyze this HTTP request and classify its intent.

Request:
- Endpoint: {request_data.get('endpoint', 'unknown')}
- Method: {request_data.get('method', 'GET')}
- User Agent: {request_data.get('user_agent', 'unknown')}

Classify as one of: reconnaissance, enumeration, exploitation, data_access, normal, or suspicious.

Respond in JSON format:
{{"intent": "classification", "confidence": 0.0-1.0, "reasoning": "explanation"}}"""
        
        try:
            response = self._generate_response(prompt, json_mode=True)
            if isinstance(response, dict):
                return response
            # Try to parse JSON from text response
            if isinstance(response, str):
                import re
                json_match = re.search(r'\{[^}]+\}', response)
                if json_match:
                    return json.loads(json_match.group())
            return {"intent": "unknown", "confidence": 0.5, "reasoning": response}
        except Exception as e:
            self.logger.error(f"Intent classification failed: {e}")
            return {"intent": "unknown", "confidence": 0.0, "reasoning": str(e)}
    
    def _build_analysis_prompt(self, request_data: Dict[str, Any], context: Optional[List[Dict]] = None) -> str:
        """Build prompt for request pattern analysis"""
        prompt = f"""You are a cybersecurity AI analyzing HTTP request patterns for GTG-1002 style autonomous AI attacks.

Current Request:
- Endpoint: {request_data.get('endpoint', 'unknown')}
- Method: {request_data.get('method', 'GET')}
- IP Address: {request_data.get('ip_address', 'unknown')}
- User Agent: {request_data.get('user_agent', 'unknown')}
- Timestamp: {request_data.get('timestamp', 'unknown')}"""
        
        if context:
            prompt += "\n\nRecent Request Context:"
            for i, req in enumerate(context[-5:], 1):  # Last 5 requests
                prompt += f"\n{i}. {req.get('endpoint', 'unknown')} from {req.get('ip_address', 'unknown')}"
        
        prompt += """

Analyze this request pattern and identify:
1. Is this part of an automated attack pattern?
2. What attack technique might this represent?
3. What is the threat level (low/medium/high)?

Respond with a brief analysis (2-3 sentences):"""
        
        return prompt
    
    def _generate_response(self, prompt: str, json_mode: bool = False) -> Dict[str, Any]:
        """
        Generate LLM response
        
        Args:
            prompt: Input prompt
            json_mode: Whether to expect JSON response
            
        Returns:
            Response dictionary
        """
        if not self.client:
            raise RuntimeError("Ollama client not initialized")
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            )
            
            # Extract response text - handle both dict and object responses
            if hasattr(response, 'response'):
                # Handle GenerateResponse object
                response_text = response.response
            elif isinstance(response, dict):
                # Handle dict response
                response_text = response.get('response', '')
            else:
                # Fallback
                response_text = str(response)
            
            if json_mode:
                # Try to parse as JSON
                try:
                    return json.loads(response_text)
                except:
                    return {"response": response_text}
            
            return {"response": response_text}
        except Exception as e:
            self.logger.error(f"LLM generation failed: {e}")
            raise
    
    def _extract_confidence(self, response: Dict[str, Any]) -> float:
        """Extract confidence score from response if available"""
        # Simple heuristic - could be enhanced
        text = response.get('response', '').lower()
        if 'high confidence' in text or 'certain' in text:
            return 0.9
        elif 'medium confidence' in text or 'likely' in text:
            return 0.6
        elif 'low confidence' in text or 'uncertain' in text:
            return 0.3
        return 0.5
    
    @lru_cache(maxsize=100)
    def _cached_analysis(self, prompt_hash: str) -> Optional[Dict[str, Any]]:
        """Cached analysis (placeholder - would need proper caching implementation)"""
        return None

