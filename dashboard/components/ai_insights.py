"""
AI Insights Panel - Dashboard component for AI-generated insights
"""
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from ai_tools.utils.models import Detection
from ai_tools.ai_analysis.threat_analyzer import AIThreatAnalyzer
from ai_tools.ai_analysis.security_assistant import SecurityAssistant


def create_threat_explanation_card(detection: Detection, ai_analyzer: Optional[AIThreatAnalyzer] = None) -> Dict[str, Any]:
    """
    Create threat explanation card with AI insights
    
    Args:
        detection: Detection object
        ai_analyzer: AIThreatAnalyzer instance
        
    Returns:
        Dictionary with explanation card data
    """
    if not ai_analyzer:
        return {
            "title": f"{detection.pattern_type.value.replace('_', ' ').title()}",
            "explanation": f"Threat score: {detection.threat_score}/100",
            "ai_enhanced": False
        }
    
    try:
        ai_analysis = ai_analyzer.analyze_detection(detection)
        
        return {
            "title": f"{detection.pattern_type.value.replace('_', ' ').title()} Detected",
            "explanation": ai_analysis.get("explanation", "Threat detected"),
            "recommendations": ai_analysis.get("recommendations", []),
            "intent": ai_analysis.get("intent", "unknown"),
            "intent_confidence": ai_analysis.get("intent_confidence", 0.0),
            "ai_enhanced": ai_analysis.get("ai_enhanced", False),
            "model": ai_analysis.get("model_used", "unknown")
        }
    except Exception as e:
        return {
            "title": f"{detection.pattern_type.value.replace('_', ' ').title()}",
            "explanation": f"Threat score: {detection.threat_score}/100",
            "ai_enhanced": False,
            "error": str(e)
        }


def create_ai_recommendations_panel(detections: List[Detection], ai_analyzer: Optional[AIThreatAnalyzer] = None) -> List[Dict[str, Any]]:
    """
    Create AI recommendations panel
    
    Args:
        detections: List of detections
        ai_analyzer: AIThreatAnalyzer instance
        
    Returns:
        List of recommendation dictionaries
    """
    if not ai_analyzer or not detections:
        return []
    
    recommendations = []
    seen_patterns = set()
    
    # Get recommendations for unique patterns
    for detection in detections:
        if detection.pattern_type.value not in seen_patterns and detection.threat_level.value != "normal":
            seen_patterns.add(detection.pattern_type.value)
            try:
                ai_analysis = ai_analyzer.analyze_detection(detection)
                recs = ai_analysis.get("recommendations", [])
                for rec in recs[:3]:  # Top 3 per pattern
                    recommendations.append({
                        "pattern": detection.pattern_type.value,
                        "recommendation": rec,
                        "priority": "high" if detection.threat_level.value == "malicious" else "medium"
                    })
            except Exception as e:
                continue
    
    return recommendations


def format_ai_alert(detection: Detection, explanation: str) -> Dict[str, Any]:
    """
    Format alert with AI-generated natural language
    
    Args:
        detection: Detection object
        explanation: AI-generated explanation
        
    Returns:
        Formatted alert dictionary
    """
    return {
        "timestamp": detection.timestamp.isoformat(),
        "severity": detection.threat_level.value,
        "pattern": detection.pattern_type.value,
        "score": detection.threat_score,
        "explanation": explanation,
        "endpoint": detection.request.endpoint,
        "ip": detection.request.ip_address
    }


def generate_attack_scenario_description(pattern_type: str, details: Dict[str, Any], ai_analyzer: Optional[AIThreatAnalyzer] = None) -> str:
    """
    Generate attack scenario description using AI
    
    Args:
        pattern_type: Pattern type
        details: Detection details
        ai_analyzer: AIThreatAnalyzer instance
        
    Returns:
        Attack scenario description
    """
    if not ai_analyzer:
        return f"Attack pattern: {pattern_type}"
    
    try:
        return ai_analyzer.generate_attack_scenario(pattern_type, details)
    except Exception as e:
        return f"Attack pattern: {pattern_type}"

