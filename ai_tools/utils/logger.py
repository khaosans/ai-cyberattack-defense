"""
Structured logging for AI Pattern Detector
"""
import logging
import sys
from datetime import datetime
from typing import Optional
from .models import Detection, Alert


class DetectionLogger:
    """Structured logger for detection events"""
    
    def __init__(self, log_level: int = logging.INFO):
        """Initialize logger"""
        self.logger = logging.getLogger("ai_pattern_detector")
        self.logger.setLevel(log_level)
        
        # Create console handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(log_level)
            
            # Structured format
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_detection(self, detection: Detection):
        """Log a detection event"""
        try:
            # Safely extract values with fallbacks
            pattern_type = detection.pattern_type.value if hasattr(detection.pattern_type, 'value') else str(detection.pattern_type)
            threat_level = detection.threat_level.value if hasattr(detection.threat_level, 'value') else str(detection.threat_level)
            threat_score = getattr(detection, 'threat_score', 0)
            endpoint = getattr(detection.request, 'endpoint', 'unknown') if hasattr(detection, 'request') else 'unknown'
            ip_address = getattr(detection.request, 'ip_address', 'unknown') if hasattr(detection, 'request') else 'unknown'
            
            level = self._get_log_level(detection.threat_level)
            message = (
                f"Detection: {pattern_type} | "
                f"Score: {threat_score} | "
                f"Endpoint: {endpoint} | "
                f"IP: {ip_address}"
            )
            self.logger.log(level, message)
        except Exception as e:
            # Fallback logging if there's any error
            self.logger.warning(f"Failed to log detection: {e}")
    
    def log_alert(self, alert: Alert):
        """Log an alert event"""
        level = logging.WARNING if alert.severity == "high" else logging.INFO
        self.logger.log(level, f"ALERT [{alert.severity.upper()}]: {alert.message}")
    
    def _get_log_level(self, threat_level) -> int:
        """Map threat level to log level"""
        try:
            # Handle both enum and string values
            if hasattr(threat_level, 'value'):
                level_str = threat_level.value
            else:
                level_str = str(threat_level)
            
            mapping = {
                "normal": logging.INFO,
                "suspicious": logging.WARNING,
                "malicious": logging.ERROR
            }
            return mapping.get(level_str.lower(), logging.INFO)
        except Exception:
            return logging.INFO

