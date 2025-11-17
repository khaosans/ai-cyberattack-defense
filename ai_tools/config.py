"""
Configuration management for AI Pattern Detector
"""
import os
from typing import Dict, Any


class Config:
    """Configuration settings"""
    
    # Detection thresholds
    SUPERHUMAN_SPEED_THRESHOLD = float(os.getenv("SUPERHUMAN_SPEED_THRESHOLD", "10.0"))  # requests/second
    ENUMERATION_SEQUENCE_LENGTH = int(os.getenv("ENUMERATION_SEQUENCE_LENGTH", "5"))
    ANOMALY_Z_SCORE_THRESHOLD = float(os.getenv("ANOMALY_Z_SCORE_THRESHOLD", "2.0"))
    
    # Request history
    MAX_HISTORY_SIZE = int(os.getenv("MAX_HISTORY_SIZE", "1000"))
    SPEED_WINDOW_SECONDS = int(os.getenv("SPEED_WINDOW_SECONDS", "10"))
    
    # Dashboard
    DASHBOARD_REFRESH_RATE = int(os.getenv("DASHBOARD_REFRESH_RATE", "2"))  # seconds
    MAX_DETECTIONS_DISPLAY = int(os.getenv("MAX_DETECTIONS_DISPLAY", "100"))
    
    # Simulation
    SIMULATION_RATE = float(os.getenv("SIMULATION_RATE", "1.0"))  # requests per second
    ATTACK_INTENSITY = float(os.getenv("ATTACK_INTENSITY", "0.1"))  # 0.0 to 1.0
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Ollama AI Integration
    OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "true").lower() == "true"
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    # Default to first available model, fallback to llama3.2:3b or mistral:latest
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    AI_ANALYSIS_ENABLED = os.getenv("AI_ANALYSIS_ENABLED", "true").lower() == "true"
    AI_CACHE_ENABLED = os.getenv("AI_CACHE_ENABLED", "true").lower() == "true"
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """Get all configuration values"""
        return {
            "superhuman_speed_threshold": cls.SUPERHUMAN_SPEED_THRESHOLD,
            "enumeration_sequence_length": cls.ENUMERATION_SEQUENCE_LENGTH,
            "anomaly_z_score_threshold": cls.ANOMALY_Z_SCORE_THRESHOLD,
            "max_history_size": cls.MAX_HISTORY_SIZE,
            "speed_window_seconds": cls.SPEED_WINDOW_SECONDS,
            "dashboard_refresh_rate": cls.DASHBOARD_REFRESH_RATE,
            "max_detections_display": cls.MAX_DETECTIONS_DISPLAY,
            "simulation_rate": cls.SIMULATION_RATE,
            "attack_intensity": cls.ATTACK_INTENSITY,
            "log_level": cls.LOG_LEVEL,
            "ollama_enabled": cls.OLLAMA_ENABLED,
            "ollama_host": cls.OLLAMA_HOST,
            "ollama_model": cls.OLLAMA_MODEL,
            "ai_analysis_enabled": cls.AI_ANALYSIS_ENABLED,
            "ai_cache_enabled": cls.AI_CACHE_ENABLED
        }

