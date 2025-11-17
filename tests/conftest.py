"""
Pytest configuration and fixtures
"""
import pytest
import sys
from pathlib import Path
from datetime import datetime
from typing import Generator

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ai_tools.utils.models import Request, Detection, ThreatLevel, PatternType
from ai_tools.config import Config
from ai_tools.detection.ai_pattern_detector import AIPatternDetector
from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
from ai_tools.simulation.attack_simulator import AttackSimulator


@pytest.fixture
def config():
    """Provide test configuration"""
    return Config()


@pytest.fixture
def sample_request():
    """Create a sample request for testing"""
    return Request(
        timestamp=datetime.now(),
        ip_address="192.168.1.100",
        endpoint="/api/users/1",
        method="GET",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )


@pytest.fixture
def sample_attack_request():
    """Create a sample attack request for testing"""
    return Request(
        timestamp=datetime.now(),
        ip_address="10.0.0.1",
        endpoint="/api/admin/users",
        method="GET",
        user_agent="python-requests/2.28.0"
    )


@pytest.fixture
def detector(config):
    """Create AIPatternDetector instance"""
    return AIPatternDetector(config=config)


@pytest.fixture
def enhanced_detector(config):
    """Create EnhancedAIPatternDetector instance"""
    return EnhancedAIPatternDetector(config=config, enable_ai=False)


@pytest.fixture
def simulator():
    """Create AttackSimulator instance"""
    return AttackSimulator()


@pytest.fixture
def rapid_requests():
    """Generate rapid requests for speed testing"""
    base_time = datetime.now()
    requests = []
    for i in range(20):
        requests.append(Request(
            timestamp=base_time.replace(microsecond=i * 10000),
            ip_address="192.168.1.100",
            endpoint=f"/api/users/{i}",
            method="GET",
            user_agent="python-requests/2.28.0"
        ))
    return requests


@pytest.fixture
def enumeration_requests():
    """Generate enumeration pattern requests"""
    base_time = datetime.now()
    requests = []
    endpoints = [
        "/api/users/1",
        "/api/users/2",
        "/api/users/3",
        "/api/users/4",
        "/api/users/5"
    ]
    for i, endpoint in enumerate(endpoints):
        requests.append(Request(
            timestamp=base_time.replace(microsecond=i * 100000),
            ip_address="10.0.0.1",
            endpoint=endpoint,
            method="GET",
            user_agent="python-requests/2.28.0"
        ))
    return requests

