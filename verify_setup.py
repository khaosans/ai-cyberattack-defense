#!/usr/bin/env python3
"""
Quick Setup Verification Script
Run this after setup to verify everything is working
"""
import sys
import subprocess
from pathlib import Path

def run_check():
    """Run the environment check script"""
    print("Running environment check...")
    print("=" * 60)
    result = subprocess.run([sys.executable, "check_environment.py"], 
                          capture_output=False)
    return result.returncode == 0

def test_imports():
    """Test critical imports"""
    print("\nTesting critical imports...")
    try:
        from ai_tools.detection.ai_pattern_detector import AIPatternDetector
        from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
        from ai_tools.simulation.attack_simulator import AttackSimulator
        from dashboard.app import st  # Just check if module loads
        print("✓ All critical imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_detector():
    """Test detector initialization"""
    print("\nTesting detector initialization...")
    try:
        from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
        detector = EnhancedAIPatternDetector(enable_ai=False)
        print("✓ Detector initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Detector initialization failed: {e}")
        return False

def test_dashboard_components():
    """Test dashboard component imports"""
    print("\nTesting dashboard components...")
    try:
        from dashboard.components.threat_chart import create_threat_timeline
        from dashboard.components.alert_feed import create_alerts
        from dashboard.components.metrics_panel import get_metrics_summary
        print("✓ Dashboard components import successfully")
        return True
    except Exception as e:
        print(f"✗ Dashboard component import failed: {e}")
        return False

def main():
    """Main verification"""
    print("=" * 60)
    print("Setup Verification")
    print("=" * 60)
    print()
    
    checks = []
    
    # Run environment check
    checks.append(run_check())
    
    # Test imports
    checks.append(test_imports())
    
    # Test detector
    checks.append(test_detector())
    
    # Test dashboard components
    checks.append(test_dashboard_components())
    
    # Summary
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All verification checks passed!")
        print("\nYou're ready to start the dashboard:")
        print("  streamlit run dashboard/app.py")
        return 0
    else:
        print("❌ Some checks failed.")
        print("\nPlease review the errors above and:")
        print("  1. Run: python3 check_environment.py")
        print("  2. Check: SETUP_GUIDE.md")
        print("  3. Verify: pip install -r ai_tools/requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())

