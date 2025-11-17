"""
Enhanced AI Pattern Detector - Combines rule-based and AI-based detection
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .ai_pattern_detector import AIPatternDetector
from ..ai_analysis.threat_analyzer import AIThreatAnalyzer
from ..utils.models import Request, Detection, ThreatLevel
from ..config import Config


class EnhancedAIPatternDetector(AIPatternDetector):
    """
    Enhanced detector that combines rule-based detection with AI analysis
    
    Features:
    - Rule-based detection (inherited from AIPatternDetector)
    - AI-powered threat analysis
    - AI-powered false positive reduction
    - Context-aware threat scoring
    - Natural language alert generation
    """
    
    def __init__(self, config: Optional[Config] = None, enable_ai: bool = True):
        """
        Initialize enhanced detector
        
        Args:
            config: Configuration object
            enable_ai: Whether to enable AI analysis
        """
        super().__init__(config)
        self.enable_ai = enable_ai and getattr(config or Config(), 'AI_ANALYSIS_ENABLED', True)
        self.ai_analyzer = AIThreatAnalyzer(config=config) if self.enable_ai else None
        # Use parent's DetectionLogger (self.logger) for detection logging
        # For standard logging, use the underlying logger: self.logger.logger
        self.std_logger = logging.getLogger(__name__)
        
        # Enhanced detection storage
        self.ai_enhanced_detections: List[Dict[str, Any]] = []
    
    def analyze_request(self, request: Request) -> Detection:
        """
        Analyze request with enhanced AI capabilities
        
        Args:
            request: Request object to analyze
            
        Returns:
            Detection object with AI-enhanced analysis
        """
        # First, perform standard rule-based detection
        detection = super().analyze_request(request)
        
        # If AI is enabled and threat detected, enhance with AI analysis
        if self.enable_ai and self.ai_analyzer and detection.threat_level.value != "normal":
            try:
                # Get recent requests for context
                recent_requests = []
                if hasattr(self, 'request_history') and self.request_history:
                    recent_requests = [r["request"] for r in list(self.request_history)[-10:]]
                
                # Get AI-enhanced analysis
                ai_analysis = self.ai_analyzer.analyze_detection(
                    detection,
                    request_history=recent_requests
                )
                
                # Store AI enhancement
                self.ai_enhanced_detections.append({
                    "detection": detection,
                    "ai_analysis": ai_analysis,
                    "timestamp": datetime.now()
                })
                
                # Adjust threat score based on AI analysis if needed
                if ai_analysis.get("ai_enhanced", False):
                    # AI can provide additional context for scoring
                    intent_confidence = ai_analysis.get("intent_confidence", 0.5)
                    if intent_confidence > 0.7 and ai_analysis.get("intent") in ["reconnaissance", "enumeration", "exploitation"]:
                        # Boost threat score if AI confirms malicious intent
                        detection.threat_score = min(100, detection.threat_score + 5)
                        if detection.threat_score >= 70:
                            detection.threat_level = ThreatLevel.MALICIOUS
                    elif intent_confidence < 0.3 and ai_analysis.get("intent") == "normal":
                        # Reduce false positives if AI suggests normal intent
                        detection.threat_score = max(0, detection.threat_score - 10)
                        if detection.threat_score < 30:
                            detection.threat_level = ThreatLevel.NORMAL
                
            except Exception as e:
                self.std_logger.warning(f"AI enhancement failed, using rule-based detection: {e}")
        
        return detection
    
    def get_ai_enhanced_detection(self, detection: Detection) -> Optional[Dict[str, Any]]:
        """
        Get AI-enhanced analysis for a detection
        
        Args:
            detection: Detection object
            
        Returns:
            AI analysis dictionary or None
        """
        # Find matching enhanced detection by timestamp and endpoint
        for enhanced in self.ai_enhanced_detections:
            stored_det = enhanced["detection"]
            # Match by timestamp and endpoint (most reliable)
            if (stored_det.timestamp == detection.timestamp and 
                stored_det.request.endpoint == detection.request.endpoint and
                stored_det.request.ip_address == detection.request.ip_address):
                return enhanced.get("ai_analysis")
        return None
    
    def get_ai_recommendations(self, detection: Detection) -> List[str]:
        """
        Get AI-generated recommendations for a detection
        
        Args:
            detection: Detection object
            
        Returns:
            List of recommendations
        """
        if not self.enable_ai or not self.ai_analyzer:
            return []
        
        ai_analysis = self.get_ai_enhanced_detection(detection)
        if ai_analysis:
            return ai_analysis.get("recommendations", [])
        return []
    
    def get_threat_explanation(self, detection: Detection) -> str:
        """
        Get natural language explanation of threat
        
        Args:
            detection: Detection object
            
        Returns:
            Threat explanation string
        """
        if not self.enable_ai or not self.ai_analyzer:
            return f"Threat detected: {detection.pattern_type.value} (Score: {detection.threat_score})"
        
        ai_analysis = self.get_ai_enhanced_detection(detection)
        if ai_analysis:
            return ai_analysis.get("explanation", f"Threat: {detection.pattern_type.value}")
        
        # Generate explanation on demand
        try:
            detection_data = {
                "pattern_type": detection.pattern_type.value,
                "threat_score": detection.threat_score,
                "endpoint": detection.request.endpoint,
                "ip_address": detection.request.ip_address,
                "details": detection.details
            }
            return self.ai_analyzer.ollama.explain_threat(detection_data)
        except Exception as e:
            self.std_logger.error(f"Explanation generation failed: {e}")
            return f"Threat: {detection.pattern_type.value}"
    
    def generate_incident_report(self) -> str:
        """
        Generate AI-powered incident report
        
        Returns:
            Formatted incident report
        """
        if not self.enable_ai or not self.ai_analyzer:
            return self._generate_basic_report()
        
        try:
            return self.ai_analyzer.generate_incident_report(self.detections)
        except Exception as e:
            self.std_logger.error(f"Report generation failed: {e}")
            return self._generate_basic_report()
    
    def _generate_basic_report(self) -> str:
        """Generate basic report without AI"""
        if not self.detections:
            return "No detections."
        
        report = f"# Incident Report\n\n"
        report += f"**Total Detections:** {len(self.detections)}\n\n"
        report += f"**Threat Breakdown:**\n"
        for level in ["malicious", "suspicious", "normal"]:
            count = len([d for d in self.detections if d.threat_level.value == level])
            report += f"- {level.capitalize()}: {count}\n"
        
        return report

