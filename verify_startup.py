#!/usr/bin/env python3
"""
Startup verification script
Tests all components before dashboard launch
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def verify_imports():
    """Verify all critical imports work"""
    print("Verifying imports...")
    try:
        from ai_tools.detection.ai_pattern_detector import AIPatternDetector
        from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
        from ai_tools.simulation.attack_simulator import AttackSimulator
        from ai_tools.config import Config
        from ai_tools.utils.models import Request, Detection
        print("  ✓ Core modules imported")
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def verify_detector():
    """Verify detector initializes"""
    print("Verifying detector...")
    try:
        from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
        from ai_tools.config import Config
        config = Config()
        detector = EnhancedAIPatternDetector(config=config, enable_ai=False)
        print("  ✓ Detector initialized")
        return True
    except Exception as e:
        print(f"  ❌ Detector initialization failed: {e}")
        return False

def verify_ollama():
    """Verify Ollama connection"""
    print("Verifying Ollama...")
    try:
        from ai_tools.ai_analysis.ollama_client import OllamaClient
        from ai_tools.config import Config
        config = Config()
        client = OllamaClient(config=config)
        if client.is_available():
            print(f"  ✓ Ollama connected (Model: {client.model})")
            return True
        else:
            print("  ⚠ Ollama unavailable (will use fallback)")
            return True  # Not a failure, just unavailable
    except Exception as e:
        print(f"  ⚠ Ollama check failed: {e} (will use fallback)")
        return True  # Not a failure

def verify_logger():
    """Verify logger works"""
    print("Verifying logger...")
    try:
        from ai_tools.utils.logger import DetectionLogger
        from ai_tools.utils.models import Detection, Request, ThreatLevel, PatternType
        from datetime import datetime
        
        logger = DetectionLogger()
        # Create a test detection
        request = Request(
            timestamp=datetime.now(),
            ip_address="192.168.1.100",
            endpoint="/api/test",
            method="GET",
            user_agent="test"
        )
        detection = Detection(
            timestamp=datetime.now(),
            request=request,
            threat_score=50,
            threat_level=ThreatLevel.SUSPICIOUS,
            pattern_type=PatternType.NORMAL,
            details={}
        )
        logger.log_detection(detection)
        print("  ✓ Logger working")
        return True
    except Exception as e:
        print(f"  ❌ Logger failed: {e}")
        return False

def main():
    """Run all verifications"""
    print("=" * 60)
    print("Startup Verification")
    print("=" * 60)
    print()
    
    checks = [
        verify_imports(),
        verify_detector(),
        verify_logger(),
        verify_ollama(),
    ]
    
    print()
    print("=" * 60)
    if all(checks):
        print("✓ All verifications passed!")
        print("Dashboard should start successfully.")
        return 0
    else:
        print("❌ Some verifications failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

