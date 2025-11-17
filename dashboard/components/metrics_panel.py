"""
Metrics panel component for dashboard
"""
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from ai_tools.utils.models import Detection
from ai_tools.utils.helpers import calculate_statistics


def get_metrics_summary(detections: list[Detection]) -> Dict[str, Any]:
    """
    Get summary metrics for display
    
    Args:
        detections: List of detection objects
        
    Returns:
        Dictionary with metrics
    """
    stats = calculate_statistics(detections, window_minutes=5)
    
    return {
        "total_detections": stats["total_detections"],
        "malicious_count": stats["threat_levels"].get("malicious", 0),
        "suspicious_count": stats["threat_levels"].get("suspicious", 0),
        "normal_count": stats["threat_levels"].get("normal", 0),
        "avg_threat_score": round(stats["avg_threat_score"], 1),
        "peak_threat_score": stats["peak_threat_score"],
        "pattern_types": stats["pattern_types"]
    }


def format_metric_value(value: Any, unit: str = "") -> str:
    """Format metric value for display"""
    if isinstance(value, float):
        return f"{value:.1f}{unit}"
    return f"{value}{unit}"

