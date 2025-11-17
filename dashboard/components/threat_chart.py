"""
Threat chart component for dashboard
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List
from datetime import datetime, timedelta
import pandas as pd
import sys
from pathlib import Path
from functools import lru_cache

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from ai_tools.utils.models import Detection


def create_threat_timeline(detections: List[Detection], window_minutes: int = 10) -> go.Figure:
    """
    Create threat score timeline chart
    
    Args:
        detections: List of detection objects
        window_minutes: Time window to display
        
    Returns:
        Plotly figure
    """
    if not detections:
        # Return empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No detections yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Filter by time window
    cutoff = datetime.now() - timedelta(minutes=window_minutes)
    recent = [d for d in detections if d.timestamp >= cutoff]
    
    if not recent:
        fig = go.Figure()
        fig.add_annotation(
            text="No recent detections",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Prepare data
    timestamps = [d.timestamp for d in recent]
    threat_scores = [d.threat_score for d in recent]
    threat_levels = [d.threat_level.value for d in recent]
    
    # Create figure
    fig = go.Figure()
    
    # Color mapping
    colors = {
        "normal": "green",
        "suspicious": "orange",
        "malicious": "red"
    }
    
    # Add scatter plot with color coding
    for level in ["normal", "suspicious", "malicious"]:
        indices = [i for i, l in enumerate(threat_levels) if l == level]
        if indices:
            fig.add_trace(go.Scatter(
                x=[timestamps[i] for i in indices],
                y=[threat_scores[i] for i in indices],
                mode='markers+lines',
                name=level.capitalize(),
                marker=dict(color=colors[level], size=8),
                line=dict(color=colors[level], width=2)
            ))
    
    # Add threshold lines
    fig.add_hline(y=30, line_dash="dash", line_color="green", 
                  annotation_text="Normal Threshold", annotation_position="right")
    fig.add_hline(y=70, line_dash="dash", line_color="red", 
                  annotation_text="Malicious Threshold", annotation_position="right")
    
    fig.update_layout(
        title="Threat Score Timeline",
        xaxis_title="Time",
        yaxis_title="Threat Score",
        hovermode='closest',
        height=400,
        showlegend=True
    )
    
    return fig


def create_pattern_distribution(detections: List[Detection]) -> go.Figure:
    """
    Create pattern type distribution chart
    
    Args:
        detections: List of detection objects
        
    Returns:
        Plotly figure
    """
    if not detections:
        fig = go.Figure()
        fig.add_annotation(
            text="No detections yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Count pattern types
    pattern_counts = {}
    for detection in detections:
        pattern = detection.pattern_type.value
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=list(pattern_counts.keys()),
            y=list(pattern_counts.values()),
            marker_color=['#2ecc71', '#f39c12', '#e74c3c', '#3498db'][:len(pattern_counts)]
        )
    ])
    
    fig.update_layout(
        title="Attack Pattern Distribution",
        xaxis_title="Pattern Type",
        yaxis_title="Count",
        height=300
    )
    
    return fig


def create_threat_gauge(current_score: int) -> go.Figure:
    """
    Create threat level gauge
    
    Args:
        current_score: Current threat score (0-100)
        
    Returns:
        Plotly figure
    """
    # Determine color based on score
    if current_score < 30:
        color = "green"
    elif current_score < 70:
        color = "orange"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Current Threat Level"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig

