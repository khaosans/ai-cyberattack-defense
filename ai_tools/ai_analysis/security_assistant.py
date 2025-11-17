"""
AI Security Assistant - AI-powered security advisor using Ollama
"""
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path

from .ollama_client import OllamaClient
from ..config import Config


class SecurityAssistant:
    """
    AI-powered security advisor
    
    Features:
    - Answers questions about threats
    - Explains detection logic
    - Provides security recommendations
    - Generates incident reports
    """
    
    def __init__(self, ollama_client: Optional[OllamaClient] = None, config: Optional[Config] = None):
        """
        Initialize Security Assistant
        
        Args:
            ollama_client: OllamaClient instance
            config: Configuration object
        """
        self.config = config or Config()
        self.ollama = ollama_client or OllamaClient(config=self.config)
        self.logger = logging.getLogger(__name__)
        
        # Load threat intelligence context
        self.threat_context = self._load_threat_context()
    
    def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Answer security-related questions
        
        Args:
            question: User question
            context: Additional context (detections, requests, etc.)
            
        Returns:
            Answer with sources and confidence
        """
        if not self.ollama.is_available():
            return {
                "answer": "AI assistant unavailable. Please ensure Ollama is running.",
                "confidence": 0.0,
                "sources": []
            }
        
        # Build context-aware prompt
        prompt = self._build_qa_prompt(question, context)
        
        try:
            response = self.ollama._generate_response(prompt)
            answer = response.get('response', 'Unable to generate answer.')
            
            return {
                "answer": answer,
                "confidence": 0.8,  # Could be enhanced with LLM confidence extraction
                "sources": ["GTG-1002 Threat Analysis", "AI Pattern Detector"],
                "model": self.ollama.model
            }
        except Exception as e:
            self.logger.error(f"Question answering failed: {e}")
            return {
                "answer": f"Error generating answer: {str(e)}",
                "confidence": 0.0,
                "sources": []
            }
    
    def explain_detection_logic(self, pattern_type: str) -> str:
        """
        Explain how detection logic works for a pattern type
        
        Args:
            pattern_type: Type of pattern to explain
            
        Returns:
            Explanation of detection logic
        """
        if not self.ollama.is_available():
            return f"Detection logic for {pattern_type}: Rule-based pattern matching."
        
        prompt = f"""Explain how the AI Pattern Detector identifies {pattern_type} attacks.

Focus on:
1. What indicators are detected
2. How the detection algorithm works
3. Why this pattern indicates a threat

Keep it technical but clear (3-4 sentences):"""
        
        try:
            response = self.ollama._generate_response(prompt)
            return response.get('response', f'Detection logic for {pattern_type}')
        except Exception as e:
            self.logger.error(f"Detection explanation failed: {e}")
            return f"Detection logic: {pattern_type} pattern matching"
    
    def provide_recommendations(self, threat_level: str, pattern_type: str) -> List[Dict[str, Any]]:
        """
        Provide security recommendations based on threat
        
        Args:
            threat_level: Threat level (normal, suspicious, malicious)
            pattern_type: Type of attack pattern
            
        Returns:
            List of recommendations with priorities
        """
        if not self.ollama.is_available():
            return self._get_basic_recommendations(threat_level, pattern_type)
        
        prompt = f"""As a cybersecurity expert, provide specific security recommendations for this threat:

Threat Level: {threat_level}
Pattern Type: {pattern_type}

Provide 3-5 prioritized recommendations. Format as JSON array:
[
  {{"priority": "high/medium/low", "action": "specific action", "rationale": "why this helps"}},
  ...
]"""
        
        try:
            response = self.ollama._generate_response(prompt, json_mode=True)
            
            if isinstance(response, list):
                return response
            elif isinstance(response, dict) and 'recommendations' in response:
                return response['recommendations']
            else:
                # Fallback to basic recommendations
                return self._get_basic_recommendations(threat_level, pattern_type)
        except Exception as e:
            self.logger.error(f"Recommendation generation failed: {e}")
            return self._get_basic_recommendations(threat_level, pattern_type)
    
    def generate_incident_summary(self, detections: List[Dict[str, Any]]) -> str:
        """
        Generate incident summary from detections
        
        Args:
            detections: List of detection dictionaries
            
        Returns:
            Formatted incident summary
        """
        if not self.ollama.is_available():
            return self._generate_basic_summary(detections)
        
        if not detections:
            return "No incidents detected."
        
        # Summarize
        summary_data = {
            "count": len(detections),
            "malicious": len([d for d in detections if d.get('threat_level') == 'malicious']),
            "patterns": {}
        }
        
        for det in detections:
            pattern = det.get('pattern_type', 'unknown')
            summary_data["patterns"][pattern] = summary_data["patterns"].get(pattern, 0) + 1
        
        prompt = f"""Generate a concise incident summary for security team.

Incident Summary:
- Total Detections: {summary_data['count']}
- Malicious Threats: {summary_data['malicious']}
- Pattern Types: {summary_data['patterns']}

Provide a 2-3 sentence executive summary:"""
        
        try:
            response = self.ollama._generate_response(prompt)
            return response.get('response', self._generate_basic_summary(detections))
        except Exception as e:
            self.logger.error(f"Summary generation failed: {e}")
            return self._generate_basic_summary(detections)
    
    def _build_qa_prompt(self, question: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Build prompt for Q&A"""
        prompt = f"""You are a cybersecurity expert assistant helping security teams understand threats and defenses.

Threat Intelligence Context:
- GTG-1002: First documented AI-orchestrated cyber espionage campaign
- Attack patterns: Superhuman speeds, systematic enumeration, behavioral anomalies
- Defense: Multi-layer approach (application, infrastructure, AI platform)

Question: {question}"""
        
        if context:
            prompt += f"\n\nAdditional Context:\n{self._format_context(context)}"
        
        prompt += "\n\nProvide a clear, helpful answer based on cybersecurity best practices:"
        
        return prompt
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context for prompt"""
        formatted = []
        if 'detections' in context:
            formatted.append(f"Recent Detections: {len(context['detections'])}")
        if 'threat_score' in context:
            formatted.append(f"Current Threat Score: {context['threat_score']}")
        return "\n".join(formatted)
    
    def _load_threat_context(self) -> str:
        """Load threat intelligence context from documents"""
        try:
            # Try to load from threat analysis document
            threat_doc_path = Path(__file__).parent.parent.parent / "Threat_Analysis_GTG-1002.md"
            if threat_doc_path.exists():
                with open(threat_doc_path, 'r') as f:
                    content = f.read()
                    # Extract key sections (first 2000 chars for context)
                    return content[:2000]
        except Exception as e:
            self.logger.warning(f"Could not load threat context: {e}")
        
        return "GTG-1002: AI-orchestrated cyber espionage campaign with 80-90% autonomous execution."
    
    def _get_basic_recommendations(self, threat_level: str, pattern_type: str) -> List[Dict[str, Any]]:
        """Get basic recommendations without AI"""
        recommendations = []
        
        if threat_level == "malicious":
            recommendations.extend([
                {
                    "priority": "high",
                    "action": "Immediately isolate affected systems",
                    "rationale": "Prevent further compromise"
                },
                {
                    "priority": "high",
                    "action": "Review and rotate credentials",
                    "rationale": "Credentials may be compromised"
                }
            ])
        
        if pattern_type == "superhuman_speed":
            recommendations.append({
                "priority": "medium",
                "action": "Implement rate limiting",
                "rationale": "Prevent high-volume automated attacks"
            })
        elif pattern_type == "systematic_enumeration":
            recommendations.append({
                "priority": "medium",
                "action": "Review endpoint security",
                "rationale": "Prevent unauthorized access"
            })
        
        return recommendations
    
    def _generate_basic_summary(self, detections: List[Dict[str, Any]]) -> str:
        """Generate basic summary without AI"""
        if not detections:
            return "No incidents."
        
        malicious = len([d for d in detections if d.get('threat_level') == 'malicious'])
        return f"Incident Summary: {len(detections)} detections, {malicious} malicious threats detected."

