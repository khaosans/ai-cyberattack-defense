"""
Helper functions for AI Pattern Detector
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
from .models import Detection, ThreatLevel


def calculate_statistics(detections: List[Detection], window_minutes: int = 5) -> Dict[str, Any]:
    """Calculate detection statistics over time window"""
    if not detections:
        return {
            "total_detections": 0,
            "threat_levels": {"normal": 0, "suspicious": 0, "malicious": 0},
            "pattern_types": {},
            "avg_threat_score": 0,
            "peak_threat_score": 0
        }
    
    # Filter by time window
    cutoff = datetime.now() - timedelta(minutes=window_minutes)
    recent = [d for d in detections if d.timestamp >= cutoff]
    
    if not recent:
        return calculate_statistics([])
    
    # Count threat levels
    threat_levels = {"normal": 0, "suspicious": 0, "malicious": 0}
    pattern_types = {}
    threat_scores = []
    
    for detection in recent:
        threat_levels[detection.threat_level.value] += 1
        pattern_type = detection.pattern_type.value
        pattern_types[pattern_type] = pattern_types.get(pattern_type, 0) + 1
        threat_scores.append(detection.threat_score)
    
    return {
        "total_detections": len(recent),
        "threat_levels": threat_levels,
        "pattern_types": pattern_types,
        "avg_threat_score": sum(threat_scores) / len(threat_scores) if threat_scores else 0,
        "peak_threat_score": max(threat_scores) if threat_scores else 0
    }


def format_threat_score(score: int) -> str:
    """Format threat score with color coding"""
    if score < 30:
        return f"🟢 {score}"
    elif score < 70:
        return f"🟡 {score}"
    else:
        return f"🔴 {score}"


def get_threat_level_from_score(score: int) -> ThreatLevel:
    """Determine threat level from score"""
    if score < 30:
        return ThreatLevel.NORMAL
    elif score < 70:
        return ThreatLevel.SUSPICIOUS
    else:
        return ThreatLevel.MALICIOUS

