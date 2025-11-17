"""
AI Pattern Detector - Detects GTG-1002 style autonomous AI attacks
"""
import numpy as np
from collections import deque
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re

from ..utils.models import Request, Detection, ThreatLevel, PatternType
from ..utils.helpers import get_threat_level_from_score
from ..utils.logger import DetectionLogger
from ..config import Config


class AIPatternDetector:
    """
    Detects AI-driven attack patterns:
    - Superhuman request speeds (thousands per second)
    - Systematic enumeration (sequential endpoint discovery)
    - Behavioral anomalies (statistical pattern detection)
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize detector"""
        self.config = config or Config()
        self.request_history = deque(maxlen=self.config.MAX_HISTORY_SIZE)
        self.detections: List[Detection] = []
        self.logger = DetectionLogger()
        
        # Statistics for anomaly detection
        self.endpoint_depths = []
        self.parameter_counts = []
        self.request_intervals = []
    
    def analyze_request(self, request: Request) -> Detection:
        """
        Analyze a request for AI-driven attack patterns
        
        Args:
            request: Request object to analyze
            
        Returns:
            Detection object with threat assessment
        """
        self.request_history.append({
            "request": request,
            "timestamp": request.timestamp
        })
        
        # Detect patterns
        speed_detection = self._detect_superhuman_speed()
        enum_detection = self._detect_systematic_enumeration()
        anomaly_detection = self._detect_behavioral_anomaly(request)
        
        # Calculate threat score
        threat_score = self._calculate_threat_score(
            speed_detection, enum_detection, anomaly_detection
        )
        
        # Determine pattern type and threat level
        pattern_type = self._determine_pattern_type(
            speed_detection, enum_detection, anomaly_detection
        )
        threat_level = get_threat_level_from_score(threat_score)
        
        # Create detection
        detection = Detection(
            timestamp=datetime.now(),
            request=request,
            threat_score=threat_score,
            threat_level=threat_level,
            pattern_type=pattern_type,
            details={
                "speed_detection": speed_detection,
                "enumeration_detection": enum_detection,
                "anomaly_detection": anomaly_detection
            }
        )
        
        self.detections.append(detection)
        
        # Safe logging - workaround for demo compatibility
        try:
            if hasattr(self.logger, 'log_detection'):
                self.logger.log_detection(detection)
            else:
                # Fallback to standard logging if DetectionLogger not available
                import logging
                logging.getLogger("ai_pattern_detector").info(
                    f"Detection: {detection.pattern_type.value} | "
                    f"Score: {detection.threat_score} | "
                    f"Endpoint: {detection.request.endpoint} | "
                    f"IP: {detection.request.ip_address}"
                )
        except (AttributeError, Exception) as e:
            # Silently continue for demo - logging is non-critical
            pass
        
        return detection
    
    def _detect_superhuman_speed(self) -> Dict[str, Any]:
        """
        Detect requests occurring at impossible human speeds
        
        Returns:
            Dictionary with detection results
        """
        if len(self.request_history) < 10:
            return {"detected": False, "requests_per_second": 0}
        
        # Get recent requests within time window
        window_start = datetime.now() - timedelta(seconds=self.config.SPEED_WINDOW_SECONDS)
        recent_requests = [
            r for r in self.request_history
            if r["timestamp"] >= window_start
        ]
        
        if len(recent_requests) < 2:
            return {"detected": False, "requests_per_second": 0}
        
        # Calculate requests per second
        time_span = (recent_requests[-1]["timestamp"] - recent_requests[0]["timestamp"]).total_seconds()
        if time_span == 0:
            time_span = 0.1  # Avoid division by zero
        
        requests_per_second = len(recent_requests) / time_span
        
        detected = requests_per_second > self.config.SUPERHUMAN_SPEED_THRESHOLD
        
        return {
            "detected": detected,
            "requests_per_second": round(requests_per_second, 2),
            "threshold": self.config.SUPERHUMAN_SPEED_THRESHOLD
        }
    
    def _detect_systematic_enumeration(self) -> Dict[str, Any]:
        """
        Detect systematic endpoint enumeration patterns
        
        Returns:
            Dictionary with detection results
        """
        if len(self.request_history) < self.config.ENUMERATION_SEQUENCE_LENGTH:
            return {"detected": False, "pattern": None}
        
        # Get recent endpoints
        recent_endpoints = [
            r["request"].endpoint for r in list(self.request_history)[-20:]
        ]
        
        # Check for sequential numeric patterns (e.g., /api/user/1, /api/user/2...)
        sequential_pattern = self._find_sequential_pattern(recent_endpoints)
        
        # Check for parameter enumeration
        param_pattern = self._find_parameter_enumeration(recent_endpoints)
        
        detected = sequential_pattern["detected"] or param_pattern["detected"]
        pattern = sequential_pattern if sequential_pattern["detected"] else param_pattern
        
        return {
            "detected": detected,
            "pattern": pattern.get("pattern") if detected else None,
            "sequence_length": pattern.get("length", 0) if detected else 0
        }
    
    def _find_sequential_pattern(self, endpoints: List[str]) -> Dict[str, Any]:
        """Find sequential numeric patterns in endpoints"""
        # Pattern: /api/user/1, /api/user/2, /api/user/3...
        base_pattern = r'(.+?)/(\d+)$'
        
        sequences = {}
        for i, endpoint in enumerate(endpoints):
            match = re.match(base_pattern, endpoint)
            if match:
                base_path = match.group(1)
                number = int(match.group(2))
                
                if base_path not in sequences:
                    sequences[base_path] = []
                sequences[base_path].append((i, number))
        
        # Check for sequential sequences
        for base_path, positions in sequences.items():
            if len(positions) >= self.config.ENUMERATION_SEQUENCE_LENGTH:
                # Check if numbers are sequential
                numbers = [p[1] for p in positions]
                if self._is_sequential(numbers):
                    return {
                        "detected": True,
                        "pattern": f"{base_path}/{{n}}",
                        "length": len(positions)
                    }
        
        return {"detected": False}
    
    def _find_parameter_enumeration(self, endpoints: List[str]) -> Dict[str, Any]:
        """Find parameter enumeration patterns"""
        # Look for patterns like ?id=1, ?id=2, ?id=3
        param_pattern = r'\?(\w+)=(\d+)'
        
        param_sequences = {}
        for endpoint in endpoints:
            match = re.search(param_pattern, endpoint)
            if match:
                param_name = match.group(1)
                param_value = int(match.group(2))
                
                if param_name not in param_sequences:
                    param_sequences[param_name] = []
                param_sequences[param_name].append(param_value)
        
        # Check for sequential parameter values
        for param_name, values in param_sequences.items():
            if len(values) >= self.config.ENUMERATION_SEQUENCE_LENGTH:
                if self._is_sequential(values):
                    return {
                        "detected": True,
                        "pattern": f"?{param_name}={{n}}",
                        "length": len(values)
                    }
        
        return {"detected": False}
    
    def _is_sequential(self, numbers: List[int], tolerance: int = 1) -> bool:
        """Check if numbers form a sequential pattern"""
        if len(numbers) < 2:
            return False
        
        sorted_numbers = sorted(set(numbers))
        if len(sorted_numbers) < self.config.ENUMERATION_SEQUENCE_LENGTH:
            return False
        
        # Check if differences are consistent (allowing for tolerance)
        diffs = [sorted_numbers[i+1] - sorted_numbers[i] for i in range(len(sorted_numbers)-1)]
        if len(set(diffs)) <= tolerance + 1:  # Allow some variation
            return True
        
        return False
    
    def _detect_behavioral_anomaly(self, request: Request) -> Dict[str, Any]:
        """
        Detect behavioral anomalies using statistical analysis
        
        Returns:
            Dictionary with detection results
        """
        # Extract features
        endpoint_depth = len(request.endpoint.split('/'))
        param_count = len(request.parameters) if request.parameters else 0
        
        # Calculate interval from previous request
        if len(self.request_history) > 1:
            prev_timestamp = self.request_history[-2]["timestamp"]
            interval = (request.timestamp - prev_timestamp).total_seconds()
            self.request_intervals.append(interval)
        else:
            interval = 1.0
        
        # Update statistics
        self.endpoint_depths.append(endpoint_depth)
        self.parameter_counts.append(param_count)
        
        # Keep statistics within reasonable size
        if len(self.endpoint_depths) > 100:
            self.endpoint_depths = self.endpoint_depths[-100:]
        if len(self.parameter_counts) > 100:
            self.parameter_counts = self.parameter_counts[-100:]
        if len(self.request_intervals) > 100:
            self.request_intervals = self.request_intervals[-100:]
        
        # Calculate z-scores if we have enough data
        if len(self.endpoint_depths) < 10:
            return {"detected": False, "z_score": 0}
        
        depth_mean = np.mean(self.endpoint_depths)
        depth_std = np.std(self.endpoint_depths) if np.std(self.endpoint_depths) > 0 else 1
        depth_z = abs((endpoint_depth - depth_mean) / depth_std)
        
        param_mean = np.mean(self.parameter_counts)
        param_std = np.std(self.parameter_counts) if np.std(self.parameter_counts) > 0 else 1
        param_z = abs((param_count - param_mean) / param_std)
        
        interval_mean = np.mean(self.request_intervals) if self.request_intervals else 1.0
        interval_std = np.std(self.request_intervals) if self.request_intervals and np.std(self.request_intervals) > 0 else 1.0
        interval_z = abs((interval - interval_mean) / interval_std) if interval_std > 0 else 0
        
        # Combined anomaly score
        max_z_score = max(depth_z, param_z, interval_z)
        
        detected = max_z_score > self.config.ANOMALY_Z_SCORE_THRESHOLD
        
        return {
            "detected": detected,
            "z_score": round(max_z_score, 2),
            "threshold": self.config.ANOMALY_Z_SCORE_THRESHOLD,
            "features": {
                "endpoint_depth_z": round(depth_z, 2),
                "parameter_count_z": round(param_z, 2),
                "interval_z": round(interval_z, 2)
            }
        }
    
    def _calculate_threat_score(
        self,
        speed_detection: Dict[str, Any],
        enum_detection: Dict[str, Any],
        anomaly_detection: Dict[str, Any]
    ) -> int:
        """
        Calculate overall threat score (0-100)
        
        Args:
            speed_detection: Speed detection results
            enum_detection: Enumeration detection results
            anomaly_detection: Anomaly detection results
            
        Returns:
            Threat score from 0 to 100
        """
        score = 0
        
        # Speed detection contributes up to 40 points
        if speed_detection["detected"]:
            rps = speed_detection.get("requests_per_second", 0)
            threshold = speed_detection.get("threshold", 10)
            # Scale based on how much over threshold
            speed_score = min(40, (rps / threshold) * 30)
            score += speed_score
        
        # Enumeration detection contributes up to 35 points
        if enum_detection["detected"]:
            seq_length = enum_detection.get("sequence_length", 0)
            enum_score = min(35, seq_length * 5)
            score += enum_score
        
        # Anomaly detection contributes up to 25 points
        if anomaly_detection["detected"]:
            z_score = anomaly_detection.get("z_score", 0)
            threshold = anomaly_detection.get("threshold", 2.0)
            anomaly_score = min(25, (z_score / threshold) * 20)
            score += anomaly_score
        
        return min(100, int(score))
    
    def _determine_pattern_type(
        self,
        speed_detection: Dict[str, Any],
        enum_detection: Dict[str, Any],
        anomaly_detection: Dict[str, Any]
    ) -> PatternType:
        """Determine primary pattern type"""
        if speed_detection["detected"]:
            return PatternType.SUPERHUMAN_SPEED
        elif enum_detection["detected"]:
            return PatternType.SYSTEMATIC_ENUMERATION
        elif anomaly_detection["detected"]:
            return PatternType.BEHAVIORAL_ANOMALY
        else:
            return PatternType.NORMAL
    
    def get_detection_stats(self, window_minutes: int = 5) -> Dict[str, Any]:
        """
        Get detection statistics for dashboard
        
        Args:
            window_minutes: Time window for statistics
            
        Returns:
            Dictionary with statistics
        """
        from ..utils.helpers import calculate_statistics
        return calculate_statistics(self.detections, window_minutes)
    
    def get_recent_detections(self, limit: int = 50) -> List[Detection]:
        """Get recent detections"""
        return self.detections[-limit:]
    
    def clear_history(self):
        """Clear detection history (for testing/reset)"""
        self.detections.clear()
        self.request_history.clear()
        self.endpoint_depths.clear()
        self.parameter_counts.clear()
        self.request_intervals.clear()

