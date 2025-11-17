"""
AI Threat Analyzer - Enhanced threat analysis using Ollama LLM
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import json

from .ollama_client import OllamaClient
from ..utils.models import Detection, Request
from ..config import Config


class AIThreatAnalyzer:
    """
    Uses Ollama LLM for enhanced threat analysis
    
    Capabilities:
    - Context-aware pattern recognition
    - Natural language threat explanations
    - Attack scenario generation
    - Response recommendation engine
    """
    
    def __init__(self, ollama_client: Optional[OllamaClient] = None, config: Optional[Config] = None):
        """
        Initialize AI Threat Analyzer
        
        Args:
            ollama_client: OllamaClient instance (creates new if None)
            config: Configuration object
        """
        self.config = config or Config()
        self.ollama = ollama_client or OllamaClient(config=self.config)
        self.logger = logging.getLogger(__name__)
        
        # Context storage for analysis
        self.request_context: List[Dict[str, Any]] = []
        self.max_context_size = 50
    
    def analyze_detection(self, detection: Detection, request_history: Optional[List[Request]] = None) -> Dict[str, Any]:
        """
        Perform AI-enhanced analysis of a detection
        
        Args:
            detection: Detection object to analyze
            request_history: Recent request history for context
            
        Returns:
            Enhanced analysis results
        """
        if not self.ollama.is_available():
            return {
                "ai_enhanced": False,
                "explanation": f"Threat detected: {detection.pattern_type.value}",
                "recommendations": []
            }
        
        # Prepare detection data
        detection_data = {
            "pattern_type": detection.pattern_type.value,
            "threat_score": detection.threat_score,
            "threat_level": detection.threat_level.value,
            "endpoint": detection.request.endpoint,
            "ip_address": detection.request.ip_address,
            "method": detection.request.method,
            "details": detection.details
        }
        
        # Prepare context
        context = None
        if request_history:
            context = [
                {
                    "endpoint": req.endpoint,
                    "ip_address": req.ip_address,
                    "timestamp": req.timestamp.isoformat()
                }
                for req in request_history[-10:]  # Last 10 requests
            ]
        
        # Get AI analysis
        ai_analysis = self.ollama.analyze_request_pattern(
            {
                "endpoint": detection.request.endpoint,
                "method": detection.request.method,
                "ip_address": detection.request.ip_address,
                "user_agent": detection.request.user_agent,
                "timestamp": detection.request.timestamp.isoformat()
            },
            context=context
        )
        
        # Get threat explanation
        explanation = self.ollama.explain_threat(detection_data)
        
        # Get response recommendations
        recommendations = self.ollama.suggest_response(detection_data)
        
        # Classify intent
        intent = self.ollama.classify_intent({
            "endpoint": detection.request.endpoint,
            "method": detection.request.method,
            "user_agent": detection.request.user_agent
        })
        
        return {
            "ai_enhanced": True,
            "explanation": explanation,
            "recommendations": recommendations,
            "intent": intent.get("intent", "unknown"),
            "intent_confidence": intent.get("confidence", 0.0),
            "intent_reasoning": intent.get("reasoning", ""),
            "ai_analysis": ai_analysis.get("analysis", {}),
            "model_used": self.ollama.model
        }
    
    def generate_attack_scenario(self, pattern_type: str, details: Dict[str, Any]) -> str:
        """
        Generate realistic attack scenario description
        
        Args:
            pattern_type: Type of attack pattern detected
            details: Detection details
            
        Returns:
            Attack scenario description
        """
        if not self.ollama.is_available():
            return f"Attack pattern detected: {pattern_type}"
        
        prompt = f"""You are a cybersecurity threat intelligence analyst. Describe a realistic attack scenario based on this detection.

Pattern Type: {pattern_type}
Details: {json.dumps(details, indent=2)}

Describe:
1. What the attacker is likely trying to accomplish
2. How this fits into a larger attack chain
3. What the next steps might be

Keep it realistic and based on GTG-1002 style autonomous AI attacks. 3-4 sentences:"""
        
        try:
            response = self.ollama._generate_response(prompt)
            return response.get('response', f'Attack scenario: {pattern_type}')
        except Exception as e:
            self.logger.error(f"Attack scenario generation failed: {e}")
            return f"Attack pattern: {pattern_type}"
    
    def generate_incident_report(self, detections: List[Detection]) -> str:
        """
        Generate incident report from detections
        
        Args:
            detections: List of detection objects
            
        Returns:
            Formatted incident report
        """
        if not self.ollama.is_available():
            return self._generate_basic_report(detections)
        
        if not detections:
            return "No detections to report."
        
        # Summarize detections
        summary = {
            "total": len(detections),
            "malicious": len([d for d in detections if d.threat_level.value == "malicious"]),
            "suspicious": len([d for d in detections if d.threat_level.value == "suspicious"]),
            "patterns": {}
        }
        
        for detection in detections:
            pattern = detection.pattern_type.value
            summary["patterns"][pattern] = summary["patterns"].get(pattern, 0) + 1
        
        prompt = f"""Generate a professional cybersecurity incident report based on these detections.

Summary:
- Total Detections: {summary['total']}
- Malicious: {summary['malicious']}
- Suspicious: {summary['suspicious']}
- Pattern Types: {json.dumps(summary['patterns'], indent=2)}

Recent Detections:
{chr(10).join([f"- {d.pattern_type.value} (Score: {d.threat_score}) from {d.request.ip_address} at {d.request.endpoint}" for d in detections[-10:]])}

Generate a professional incident report with:
1. Executive Summary
2. Threat Assessment
3. Affected Systems
4. Recommended Actions

Format as markdown:"""
        
        try:
            response = self.ollama._generate_response(prompt)
            return response.get('response', self._generate_basic_report(detections))
        except Exception as e:
            self.logger.error(f"Incident report generation failed: {e}")
            return self._generate_basic_report(detections)
    
    def _generate_basic_report(self, detections: List[Detection]) -> str:
        """Generate basic report without AI"""
        if not detections:
            return "No detections."
        
        report = f"# Incident Report\n\n"
        report += f"**Total Detections:** {len(detections)}\n\n"
        report += f"**Threat Levels:**\n"
        report += f"- Malicious: {len([d for d in detections if d.threat_level.value == 'malicious'])}\n"
        report += f"- Suspicious: {len([d for d in detections if d.threat_level.value == 'suspicious'])}\n\n"
        report += f"**Recent Detections:**\n"
        for d in detections[-10:]:
            report += f"- {d.pattern_type.value} (Score: {d.threat_score}) from {d.request.ip_address}\n"
        
        return report
    
    def update_context(self, request: Request):
        """Update request context for analysis"""
        self.request_context.append({
            "endpoint": request.endpoint,
            "ip_address": request.ip_address,
            "timestamp": request.timestamp.isoformat(),
            "method": request.method
        })
        
        # Keep context size manageable
        if len(self.request_context) > self.max_context_size:
            self.request_context = self.request_context[-self.max_context_size:]

