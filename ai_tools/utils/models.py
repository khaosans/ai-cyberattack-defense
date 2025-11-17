"""
Data models for AI Pattern Detector
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class ThreatLevel(Enum):
    """Threat level enumeration"""
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"


class PatternType(Enum):
    """Attack pattern type enumeration"""
    SUPERHUMAN_SPEED = "superhuman_speed"
    SYSTEMATIC_ENUMERATION = "systematic_enumeration"
    BEHAVIORAL_ANOMALY = "behavioral_anomaly"
    NORMAL = "normal"


@dataclass
class Request:
    """Represents an HTTP request"""
    timestamp: datetime
    ip_address: str
    endpoint: str
    method: str
    user_agent: str
    parameters: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "ip_address": self.ip_address,
            "endpoint": self.endpoint,
            "method": self.method,
            "user_agent": self.user_agent,
            "parameters": self.parameters or {}
        }


@dataclass
class Detection:
    """Represents a threat detection"""
    timestamp: datetime
    request: Request
    threat_score: int
    threat_level: ThreatLevel
    pattern_type: PatternType
    details: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "request": self.request.to_dict(),
            "threat_score": self.threat_score,
            "threat_level": self.threat_level.value,
            "pattern_type": self.pattern_type.value,
            "details": self.details
        }


@dataclass
class Alert:
    """Represents a security alert"""
    timestamp: datetime
    severity: str
    message: str
    detection: Detection
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "severity": self.severity,
            "message": self.message,
            "detection": self.detection.to_dict()
        }

