"""
Threat Correlation Component - Shows similar attacks and threat clusters
"""
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from ai_tools.utils.models import Detection


def create_similar_attacks_panel(similar_detections: List[Detection], current_detection: Detection) -> Dict[str, Any]:
    """
    Create panel showing similar attacks
    
    Args:
        similar_detections: List of similar Detection objects
        current_detection: Current detection being analyzed
        
    Returns:
        Dictionary with panel data
    """
    if not similar_detections:
        return {
            "has_similar": False,
            "count": 0,
            "similar": []
        }
    
    similar_data = []
    for det in similar_detections:
        # Skip if it's the same detection
        if (det.timestamp == current_detection.timestamp and 
            det.request.endpoint == current_detection.request.endpoint):
            continue
        
        similar_data.append({
            "timestamp": det.timestamp,
            "threat_score": det.threat_score,
            "threat_level": det.threat_level.value,
            "pattern_type": det.pattern_type.value,
            "endpoint": det.request.endpoint,
            "ip_address": det.request.ip_address,
            "time_ago": _format_time_ago(det.timestamp)
        })
    
    return {
        "has_similar": len(similar_data) > 0,
        "count": len(similar_data),
        "similar": similar_data
    }


def create_threat_cluster_panel(clusters: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create panel showing threat clusters
    
    Args:
        clusters: List of cluster dictionaries from vector DB
        
    Returns:
        Dictionary with cluster panel data
    """
    if not clusters:
        return {
            "has_clusters": False,
            "count": 0,
            "clusters": []
        }
    
    cluster_data = []
    for cluster in clusters:
        representative = cluster.get('representative', {})
        metadata = representative.get('metadata', {})
        
        cluster_data.append({
            "size": cluster.get('size', 0),
            "pattern_type": metadata.get('pattern_type', 'unknown'),
            "threat_level": metadata.get('threat_level', 'unknown'),
            "representative_endpoint": metadata.get('endpoint', 'unknown'),
            "representative_ip": metadata.get('ip_address', 'unknown'),
            "members": cluster.get('members', [])
        })
    
    return {
        "has_clusters": len(cluster_data) > 0,
        "count": len(cluster_data),
        "clusters": cluster_data
    }


def _format_time_ago(timestamp) -> str:
    """Format timestamp as time ago string"""
    from datetime import datetime
    now = datetime.now()
    diff = now - timestamp
    
    if diff.total_seconds() < 60:
        return f"{int(diff.total_seconds())}s ago"
    elif diff.total_seconds() < 3600:
        return f"{int(diff.total_seconds() / 60)}m ago"
    elif diff.total_seconds() < 86400:
        return f"{int(diff.total_seconds() / 3600)}h ago"
    else:
        return f"{int(diff.total_seconds() / 86400)}d ago"

