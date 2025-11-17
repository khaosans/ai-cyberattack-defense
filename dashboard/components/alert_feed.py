"""
Alert feed component for dashboard
"""
from typing import List
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from ai_tools.utils.models import Detection, Alert


def create_alerts(detections: List[Detection], limit: int = 20) -> List[Alert]:
    """
    Create alerts from detections
    
    Args:
        detections: List of detection objects
        limit: Maximum number of alerts to return
        
    Returns:
        List of Alert objects
    """
    alerts = []
    
    # Filter for high-severity detections
    high_severity = [d for d in detections if d.threat_level.value in ["suspicious", "malicious"]]
    
    # Sort by timestamp (most recent first)
    high_severity.sort(key=lambda x: x.timestamp, reverse=True)
    
    for detection in high_severity[:limit]:
        # Create alert message
        if detection.pattern_type.value == "superhuman_speed":
            message = f"Superhuman request speed detected: {detection.details.get('speed_detection', {}).get('requests_per_second', 0)} req/s"
        elif detection.pattern_type.value == "systematic_enumeration":
            message = f"Systematic enumeration detected: {detection.details.get('enumeration_detection', {}).get('pattern', 'unknown pattern')}"
        elif detection.pattern_type.value == "behavioral_anomaly":
            message = f"Behavioral anomaly detected: Z-score {detection.details.get('anomaly_detection', {}).get('z_score', 0)}"
        else:
            message = f"Threat detected: {detection.pattern_type.value}"
        
        alert = Alert(
            timestamp=detection.timestamp,
            severity="high" if detection.threat_level.value == "malicious" else "medium",
            message=message,
            detection=detection
        )
        alerts.append(alert)
    
    return alerts


def get_alert_color(severity: str) -> str:
    """Get color for alert severity"""
    colors = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }
    return colors.get(severity, "⚪")


def format_alert_time(timestamp: datetime) -> str:
    """Format alert timestamp for display"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.total_seconds() < 60:
        return f"{int(diff.total_seconds())}s ago"
    elif diff.total_seconds() < 3600:
        return f"{int(diff.total_seconds() / 60)}m ago"
    else:
        return timestamp.strftime("%H:%M:%S")

