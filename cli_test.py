#!/usr/bin/env python3
"""
CLI Tool for Testing AI Pattern Detector
Easy way to test detection system without dashboard
"""
import argparse
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
from ai_tools.simulation.attack_simulator import AttackSimulator
from ai_tools.utils.models import Detection, Request
from ai_tools.config import Config


def print_detection(detection: Detection, index: int):
    """Print detection in a formatted way"""
    threat_emoji = {
        "normal": "🟢",
        "suspicious": "🟡",
        "malicious": "🔴"
    }
    emoji = threat_emoji.get(detection.threat_level.value, "⚪")
    
    print(f"\n[{index}] {emoji} {detection.threat_level.value.upper()}")
    print(f"    Score: {detection.threat_score}/100")
    print(f"    Pattern: {detection.pattern_type.value}")
    print(f"    Endpoint: {detection.request.endpoint}")
    print(f"    IP: {detection.request.ip_address}")
    print(f"    Time: {detection.timestamp.strftime('%H:%M:%S')}")


def test_normal_traffic(count: int = 10):
    """Test with normal traffic"""
    print(f"\n{'='*60}")
    print(f"Testing with NORMAL traffic ({count} requests)")
    print(f"{'='*60}\n")
    
    detector = EnhancedAIPatternDetector(enable_ai=False)
    simulator = AttackSimulator()
    
    detections: List[Detection] = []
    for i in range(count):
        request = simulator.generate_normal_request()
        detection = detector.analyze_request(request)
        detections.append(detection)
        print_detection(detection, i + 1)
        time.sleep(0.5)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total Requests: {len(detections)}")
    print(f"Normal: {sum(1 for d in detections if d.threat_level.value == 'normal')}")
    print(f"Suspicious: {sum(1 for d in detections if d.threat_level.value == 'suspicious')}")
    print(f"Malicious: {sum(1 for d in detections if d.threat_level.value == 'malicious')}")
    print(f"Avg Threat Score: {sum(d.threat_score for d in detections) / len(detections):.1f}")


def test_attack_traffic(count: int = 20):
    """Test with attack traffic"""
    print(f"\n{'='*60}")
    print(f"Testing with ATTACK traffic ({count} requests)")
    print(f"{'='*60}\n")
    
    detector = EnhancedAIPatternDetector(enable_ai=False)
    simulator = AttackSimulator()
    simulator.start_attack()
    
    detections: List[Detection] = []
    attack_sequence = 0
    for i in range(count):
        request = simulator.generate_attack_request(attack_sequence + 1)
        attack_sequence += 1
        detection = detector.analyze_request(request)
        detections.append(detection)
        print_detection(detection, i + 1)
        time.sleep(0.1)  # Fast requests to simulate attack speed
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total Requests: {len(detections)}")
    print(f"Normal: {sum(1 for d in detections if d.threat_level.value == 'normal')}")
    print(f"Suspicious: {sum(1 for d in detections if d.threat_level.value == 'suspicious')}")
    print(f"Malicious: {sum(1 for d in detections if d.threat_level.value == 'malicious')}")
    print(f"Avg Threat Score: {sum(d.threat_score for d in detections) / len(detections):.1f}")
    
    # Show detected threats
    threats = [d for d in detections if d.threat_level.value != 'normal']
    if threats:
        print(f"\n🚨 DETECTED THREATS: {len(threats)}")
        for threat in threats[:5]:  # Show first 5
            print(f"  - {threat.pattern_type.value} (Score: {threat.threat_score})")
    else:
        print("\n⚠️  No threats detected - check detection thresholds!")


def test_mixed_traffic(count: int = 30, attack_ratio: float = 0.3):
    """Test with mixed normal and attack traffic"""
    print(f"\n{'='*60}")
    print(f"Testing with MIXED traffic ({count} requests, {attack_ratio*100:.0f}% attack)")
    print(f"{'='*60}\n")
    
    detector = EnhancedAIPatternDetector(enable_ai=False)
    simulator = AttackSimulator()
    
    detections: List[Detection] = []
    attack_sequence = 0
    
    import random
    for i in range(count):
        if random.random() < attack_ratio:
            request = simulator.generate_attack_request(attack_sequence + 1)
            attack_sequence += 1
            time.sleep(0.05)  # Fast for attacks
        else:
            request = simulator.generate_normal_request()
            time.sleep(0.5)  # Normal speed
        
        detection = detector.analyze_request(request)
        detections.append(detection)
        print_detection(detection, i + 1)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total Requests: {len(detections)}")
    print(f"Normal: {sum(1 for d in detections if d.threat_level.value == 'normal')}")
    print(f"Suspicious: {sum(1 for d in detections if d.threat_level.value == 'suspicious')}")
    print(f"Malicious: {sum(1 for d in detections if d.threat_level.value == 'malicious')}")
    print(f"Avg Threat Score: {sum(d.threat_score for d in detections) / len(detections):.1f}")


def test_single_request(endpoint: str, ip: str = "198.51.100.42"):
    """Test a single custom request"""
    print(f"\n{'='*60}")
    print(f"Testing SINGLE request")
    print(f"{'='*60}\n")
    
    detector = EnhancedAIPatternDetector(enable_ai=False)
    
    request = Request(
        timestamp=datetime.now(),
        endpoint=endpoint,
        ip_address=ip,
        method="GET",
        user_agent="Claude-Code-Agent/1.0",
        parameters=None
    )
    
    detection = detector.analyze_request(request)
    print_detection(detection, 1)
    
    print(f"\n{'='*60}")
    print("DETAILS")
    print(f"{'='*60}")
    if detection.details:
        if 'speed_detection' in detection.details:
            speed = detection.details['speed_detection']
            print(f"Speed Detection: {speed.get('detected', False)}")
            print(f"  Requests/sec: {speed.get('requests_per_second', 0)}")
        if 'enumeration_detection' in detection.details:
            enum = detection.details['enumeration_detection']
            print(f"Enumeration Detection: {enum.get('detected', False)}")
            if enum.get('pattern'):
                print(f"  Pattern: {enum.get('pattern')}")
        if 'anomaly_detection' in detection.details:
            anomaly = detection.details['anomaly_detection']
            print(f"Anomaly Detection: {anomaly.get('detected', False)}")
            print(f"  Z-Score: {anomaly.get('z_score', 0)}")


def continuous_test(duration: int = 60, attack_intensity: float = 0.5):
    """Run continuous test for specified duration"""
    print(f"\n{'='*60}")
    print(f"CONTINUOUS TEST - Running for {duration} seconds")
    print(f"Attack Intensity: {attack_intensity*100:.0f}%")
    print(f"{'='*60}\n")
    
    detector = EnhancedAIPatternDetector(enable_ai=False)
    simulator = AttackSimulator()
    
    if attack_intensity > 0:
        simulator.start_attack()
    
    detections: List[Detection] = []
    start_time = time.time()
    request_count = 0
    
    try:
        while time.time() - start_time < duration:
            request = next(simulator.generate_requests(attack_intensity=attack_intensity))
            detection = detector.analyze_request(request)
            detections.append(detection)
            request_count += 1
            
            # Print only threats
            if detection.threat_level.value != 'normal':
                print_detection(detection, request_count)
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"Duration: {time.time() - start_time:.1f} seconds")
    print(f"Total Requests: {request_count}")
    print(f"Normal: {sum(1 for d in detections if d.threat_level.value == 'normal')}")
    print(f"Suspicious: {sum(1 for d in detections if d.threat_level.value == 'suspicious')}")
    print(f"Malicious: {sum(1 for d in detections if d.threat_level.value == 'malicious')}")
    if detections:
        print(f"Avg Threat Score: {sum(d.threat_score for d in detections) / len(detections):.1f}")


def main():
    parser = argparse.ArgumentParser(
        description="CLI Tool for Testing AI Pattern Detector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test with normal traffic
  python cli_test.py normal --count 10
  
  # Test with attack traffic
  python cli_test.py attack --count 20
  
  # Test with mixed traffic
  python cli_test.py mixed --count 30 --ratio 0.3
  
  # Test single request
  python cli_test.py single --endpoint "/api/user/123"
  
  # Continuous test for 60 seconds
  python cli_test.py continuous --duration 60 --intensity 0.5
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Test mode')
    
    # Normal traffic test
    normal_parser = subparsers.add_parser('normal', help='Test with normal traffic')
    normal_parser.add_argument('--count', type=int, default=10, help='Number of requests')
    
    # Attack traffic test
    attack_parser = subparsers.add_parser('attack', help='Test with attack traffic')
    attack_parser.add_argument('--count', type=int, default=20, help='Number of requests')
    
    # Mixed traffic test
    mixed_parser = subparsers.add_parser('mixed', help='Test with mixed traffic')
    mixed_parser.add_argument('--count', type=int, default=30, help='Number of requests')
    mixed_parser.add_argument('--ratio', type=float, default=0.3, help='Attack ratio (0.0 to 1.0)')
    
    # Single request test
    single_parser = subparsers.add_parser('single', help='Test single request')
    single_parser.add_argument('--endpoint', type=str, required=True, help='Endpoint to test')
    single_parser.add_argument('--ip', type=str, default='198.51.100.42', help='IP address')
    
    # Continuous test
    continuous_parser = subparsers.add_parser('continuous', help='Run continuous test')
    continuous_parser.add_argument('--duration', type=int, default=60, help='Duration in seconds')
    continuous_parser.add_argument('--intensity', type=float, default=0.5, help='Attack intensity (0.0 to 1.0)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'normal':
            test_normal_traffic(args.count)
        elif args.command == 'attack':
            test_attack_traffic(args.count)
        elif args.command == 'mixed':
            test_mixed_traffic(args.count, args.ratio)
        elif args.command == 'single':
            test_single_request(args.endpoint, args.ip)
        elif args.command == 'continuous':
            continuous_test(args.duration, args.intensity)
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

