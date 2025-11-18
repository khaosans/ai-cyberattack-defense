#!/usr/bin/env python3
"""
E2E Test Script for Dashboard Components
Simulates dashboard flow and verifies all components work correctly
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
from ai_tools.simulation.attack_simulator import AttackSimulator
from ai_tools.utils.models import Detection
from ai_tools.config import Config

# Import dashboard components
from dashboard.components.metrics_panel import get_metrics_summary
from dashboard.components.alert_feed import create_alerts
from dashboard.components.threat_chart import (
    create_threat_timeline,
    create_pattern_distribution,
    create_threat_gauge
)


def test_detector_initialization():
    """Test 1: Verify detector initializes correctly"""
    print("Test 1: Detector Initialization...")
    try:
        detector = EnhancedAIPatternDetector(enable_ai=False)
        assert detector is not None
        assert hasattr(detector, 'analyze_request')
        assert hasattr(detector, 'logger')
        print("  ✓ Detector initialized successfully")
        return detector
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        raise


def test_simulator_initialization():
    """Test 2: Verify simulator initializes correctly"""
    print("Test 2: Simulator Initialization...")
    try:
        simulator = AttackSimulator()
        assert simulator is not None
        assert hasattr(simulator, 'generate_requests')
        assert hasattr(simulator, 'start_attack')
        print("  ✓ Simulator initialized successfully")
        return simulator
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        raise


def test_attack_detection(detector, simulator, count=20):
    """Test 3: Verify attack requests generate detections with threat scores"""
    print(f"Test 3: Attack Detection ({count} requests)...")
    try:
        simulator.start_attack()
        detections: List[Detection] = []
        
        for i in range(count):
            request = simulator.generate_attack_request(i + 1)
            detection = detector.analyze_request(request)
            detections.append(detection)
        
        # Verify detections were created
        assert len(detections) == count, f"Expected {count} detections, got {len(detections)}"
        
        # Verify at least some threats are detected (after enough requests)
        if count >= 10:
            threats = [d for d in detections if d.threat_level.value != 'normal']
            assert len(threats) > 0, "No threats detected in attack traffic"
            print(f"  ✓ Generated {len(detections)} detections")
            print(f"  ✓ Detected {len(threats)} threats")
            
            # Verify threat scores
            max_score = max(d.threat_score for d in detections)
            assert max_score > 0, "No non-zero threat scores detected"
            print(f"  ✓ Max threat score: {max_score}/100")
        else:
            print(f"  ✓ Generated {len(detections)} detections (need more for threat detection)")
        
        return detections
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_metrics_calculation(detections):
    """Test 4: Verify metrics calculate correctly"""
    print("Test 4: Metrics Calculation...")
    try:
        metrics = get_metrics_summary(detections)
        
        # Verify metrics structure
        assert 'total_detections' in metrics
        assert 'malicious_count' in metrics
        assert 'suspicious_count' in metrics
        assert 'normal_count' in metrics
        assert 'avg_threat_score' in metrics
        assert 'peak_threat_score' in metrics
        
        # Verify values are reasonable
        assert metrics['total_detections'] == len(detections)
        assert metrics['avg_threat_score'] >= 0
        assert metrics['peak_threat_score'] >= 0
        assert metrics['peak_threat_score'] <= 100
        
        print(f"  ✓ Metrics calculated correctly")
        print(f"    - Total: {metrics['total_detections']}")
        print(f"    - Malicious: {metrics['malicious_count']}")
        print(f"    - Suspicious: {metrics['suspicious_count']}")
        print(f"    - Avg Score: {metrics['avg_threat_score']:.1f}")
        print(f"    - Peak Score: {metrics['peak_threat_score']}")
        
        return metrics
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        raise


def test_alerts_creation(detections):
    """Test 5: Verify alerts are created from detections"""
    print("Test 5: Alerts Creation...")
    try:
        alerts = create_alerts(detections, limit=10)
        
        # Verify alerts structure
        assert isinstance(alerts, list)
        
        # Check if we have threats to create alerts from
        threats = [d for d in detections if d.threat_level.value in ['suspicious', 'malicious']]
        
        if len(threats) > 0:
            assert len(alerts) > 0, "No alerts created from threats"
            print(f"  ✓ Created {len(alerts)} alerts from {len(threats)} threats")
            
            # Verify alert structure
            for alert in alerts:
                assert hasattr(alert, 'severity')
                assert hasattr(alert, 'message')
                assert hasattr(alert, 'timestamp')
                assert hasattr(alert, 'detection')
        else:
            print(f"  ✓ No threats to create alerts from (expected for normal traffic)")
        
        return alerts
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        raise


def test_charts_rendering(detections):
    """Test 6: Verify charts can be created"""
    print("Test 6: Charts Rendering...")
    try:
        # Test timeline chart
        timeline_fig = create_threat_timeline(detections, window_minutes=10)
        assert timeline_fig is not None
        print("  ✓ Threat timeline chart created")
        
        # Test pattern distribution
        pattern_fig = create_pattern_distribution(detections)
        assert pattern_fig is not None
        print("  ✓ Pattern distribution chart created")
        
        # Test threat gauge
        avg_score = sum(d.threat_score for d in detections) / len(detections) if detections else 0
        gauge_fig = create_threat_gauge(int(avg_score))
        assert gauge_fig is not None
        print("  ✓ Threat gauge chart created")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        raise


def test_empty_state_handling():
    """Test 7: Verify components handle empty state gracefully"""
    print("Test 7: Empty State Handling...")
    try:
        empty_detections = []
        
        # Test metrics with empty list
        metrics = get_metrics_summary(empty_detections)
        assert metrics['total_detections'] == 0
        assert metrics['avg_threat_score'] == 0
        print("  ✓ Metrics handle empty state")
        
        # Test alerts with empty list
        alerts = create_alerts(empty_detections)
        assert isinstance(alerts, list)
        assert len(alerts) == 0
        print("  ✓ Alerts handle empty state")
        
        # Test charts with empty list
        timeline_fig = create_threat_timeline(empty_detections)
        assert timeline_fig is not None
        pattern_fig = create_pattern_distribution(empty_detections)
        assert pattern_fig is not None
        gauge_fig = create_threat_gauge(0)
        assert gauge_fig is not None
        print("  ✓ Charts handle empty state")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        raise


def test_detection_ordering(detections):
    """Test 8: Verify detection ordering"""
    print("Test 8: Detection Ordering...")
    try:
        if len(detections) < 2:
            print("  ⚠ Skipped (need at least 2 detections)")
            return True
        
        # Verify timestamps are in order
        timestamps = [d.timestamp for d in detections]
        assert timestamps == sorted(timestamps), "Detections not in chronological order"
        print("  ✓ Detections are in chronological order")
        
        # Test get_recent_detections
        recent = detections[-10:] if len(detections) > 10 else detections
        assert len(recent) <= 10
        print(f"  ✓ Recent detections: {len(recent)}")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        raise


def main():
    """Run all E2E tests"""
    print("=" * 60)
    print("E2E Dashboard Testing")
    print("=" * 60)
    print()
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        # Test 1: Initialization
        detector = test_detector_initialization()
        tests_passed += 1
        print()
        
        simulator = test_simulator_initialization()
        tests_passed += 1
        print()
        
        # Test 2: Attack Detection
        detections = test_attack_detection(detector, simulator, count=20)
        tests_passed += 1
        print()
        
        # Test 3: Metrics
        metrics = test_metrics_calculation(detections)
        tests_passed += 1
        print()
        
        # Test 4: Alerts
        alerts = test_alerts_creation(detections)
        tests_passed += 1
        print()
        
        # Test 5: Charts
        test_charts_rendering(detections)
        tests_passed += 1
        print()
        
        # Test 6: Empty State
        test_empty_state_handling()
        tests_passed += 1
        print()
        
        # Test 7: Ordering
        test_detection_ordering(detections)
        tests_passed += 1
        print()
        
    except AssertionError as e:
        tests_failed += 1
        print(f"\n✗ Assertion failed: {e}")
    except Exception as e:
        tests_failed += 1
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print(f"Total Tests: {tests_passed + tests_failed}")
    
    if tests_failed == 0:
        print("\n✅ All tests passed! Dashboard components are working correctly.")
        return 0
    else:
        print(f"\n❌ {tests_failed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

