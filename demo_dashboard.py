#!/usr/bin/env python3
"""
Automated E2E Dashboard Demo Script
Tests all dashboard features end-to-end
"""
import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ai_tools.detection.enhanced_detector import EnhancedAIPatternDetector
from ai_tools.simulation.attack_simulator import AttackSimulator
from ai_tools.utils.database import DetectionDB
from ai_tools.utils.models import Detection
from ai_tools.config import Config


class DashboardDemo:
    """Automated dashboard demo and testing"""
    
    def __init__(self):
        self.detector = EnhancedAIPatternDetector(enable_ai=False)
        self.simulator = AttackSimulator()
        self.db = DetectionDB("demo_detections.db", enable_vector_db=True)
        self.results = []
    
    def log(self, message: str, status: str = "INFO"):
        """Log test result"""
        emoji = {"PASS": "✓", "FAIL": "✗", "INFO": "ℹ", "WARN": "⚠"}
        print(f"{emoji.get(status, '•')} [{status}] {message}")
        self.results.append({"status": status, "message": message, "timestamp": datetime.now()})
    
    def test_core_detection(self):
        """Test 1: Core detection functionality"""
        self.log("Testing core detection functionality...", "INFO")
        
        try:
            # Generate attack traffic
            self.simulator.start_attack()
            detections = []
            
            # Generate 20 attack requests
            for i in range(20):
                request = self.simulator.generate_attack_request(i + 1)
                detection = self.detector.analyze_request(request)
                detections.append(detection)
            
            # Verify detections
            if len(detections) != 20:
                self.log(f"Expected 20 detections, got {len(detections)}", "FAIL")
                return False
            
            # Check for threats
            threats = [d for d in detections if d.threat_level.value != 'normal']
            if len(threats) == 0:
                self.log("No threats detected in attack traffic", "WARN")
            else:
                self.log(f"Detected {len(threats)} threats (expected)", "PASS")
            
            # Verify threat scores
            max_score = max(d.threat_score for d in detections)
            if max_score > 0:
                self.log(f"Max threat score: {max_score}/100", "PASS")
            else:
                self.log("No non-zero threat scores detected", "WARN")
            
            self.detections = detections
            return True
            
        except Exception as e:
            self.log(f"Core detection test failed: {e}", "FAIL")
            import traceback
            traceback.print_exc()
            return False
    
    def test_database_persistence(self):
        """Test 2: Database persistence"""
        self.log("Testing database persistence...", "INFO")
        
        try:
            # Save detections to database
            saved_ids = []
            for detection in self.detections:
                detection_id = self.db.save_detection(detection)
                saved_ids.append(detection_id)
            
            self.log(f"Saved {len(saved_ids)} detections to database", "PASS")
            
            # Verify retrieval
            recent = self.db.get_recent_detections(limit=20)
            if len(recent) >= len(self.detections):
                self.log(f"Retrieved {len(recent)} detections from database", "PASS")
            else:
                self.log(f"Retrieved {len(recent)} detections (expected {len(self.detections)})", "WARN")
            
            # Test statistics
            stats = self.db.get_statistics()
            if stats['total_detections'] > 0:
                self.log(f"Database stats: {stats['total_detections']} total detections", "PASS")
            else:
                self.log("Database statistics not working", "FAIL")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"Database persistence test failed: {e}", "FAIL")
            import traceback
            traceback.print_exc()
            return False
    
    def test_vector_database(self):
        """Test 3: Vector database features"""
        self.log("Testing vector database features...", "INFO")
        
        if not self.db.vector_db:
            self.log("Vector DB not available (ChromaDB not installed)", "WARN")
            return True  # Not a failure, just not available
        
        try:
            # Test similarity search
            if len(self.detections) > 5:
                test_detection = self.detections[10]
                similar = self.db.find_similar_detections(test_detection, limit=3)
                
                if len(similar) > 0:
                    self.log(f"Similarity search found {len(similar)} similar attacks", "PASS")
                else:
                    self.log("Similarity search returned no results (may need more data)", "WARN")
            
            # Test clustering
            clusters = self.db.get_threat_clusters(limit=3)
            if clusters:
                self.log(f"Found {len(clusters)} threat clusters", "PASS")
            else:
                self.log("No clusters found (may need more diverse data)", "WARN")
            
            # Test vector DB stats
            vector_stats = self.db.vector_db.get_stats()
            if vector_stats['total_vectors'] > 0:
                self.log(f"Vector DB contains {vector_stats['total_vectors']} vectors", "PASS")
            else:
                self.log("Vector DB is empty", "WARN")
            
            return True
            
        except Exception as e:
            self.log(f"Vector database test failed: {e}", "FAIL")
            import traceback
            traceback.print_exc()
            return False
    
    def test_metrics_calculation(self):
        """Test 4: Metrics calculation"""
        self.log("Testing metrics calculation...", "INFO")
        
        try:
            from dashboard.components.metrics_panel import get_metrics_summary
            
            metrics = get_metrics_summary(self.detections)
            
            required_keys = ['total_detections', 'malicious_count', 'suspicious_count', 
                           'normal_count', 'avg_threat_score', 'peak_threat_score']
            
            for key in required_keys:
                if key not in metrics:
                    self.log(f"Missing metric: {key}", "FAIL")
                    return False
            
            self.log(f"Metrics calculated: Total={metrics['total_detections']}, "
                    f"Malicious={metrics['malicious_count']}, "
                    f"Avg Score={metrics['avg_threat_score']:.1f}", "PASS")
            
            return True
            
        except Exception as e:
            self.log(f"Metrics calculation test failed: {e}", "FAIL")
            import traceback
            traceback.print_exc()
            return False
    
    def test_charts_rendering(self):
        """Test 5: Charts rendering"""
        self.log("Testing charts rendering...", "INFO")
        
        try:
            from dashboard.components.threat_chart import (
                create_threat_timeline,
                create_pattern_distribution,
                create_threat_gauge
            )
            
            # Test timeline chart
            timeline = create_threat_timeline(self.detections, window_minutes=10)
            if timeline:
                self.log("Threat timeline chart created successfully", "PASS")
            else:
                self.log("Threat timeline chart creation failed", "FAIL")
                return False
            
            # Test pattern distribution
            pattern_dist = create_pattern_distribution(self.detections)
            if pattern_dist:
                self.log("Pattern distribution chart created successfully", "PASS")
            else:
                self.log("Pattern distribution chart creation failed", "FAIL")
                return False
            
            # Test threat gauge
            avg_score = sum(d.threat_score for d in self.detections) / len(self.detections)
            gauge = create_threat_gauge(int(avg_score))
            if gauge:
                self.log("Threat gauge chart created successfully", "PASS")
            else:
                self.log("Threat gauge chart creation failed", "FAIL")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"Charts rendering test failed: {e}", "FAIL")
            import traceback
            traceback.print_exc()
            return False
    
    def test_alerts_creation(self):
        """Test 6: Alerts creation"""
        self.log("Testing alerts creation...", "INFO")
        
        try:
            from dashboard.components.alert_feed import create_alerts
            
            alerts = create_alerts(self.detections, limit=10)
            
            threats = [d for d in self.detections if d.threat_level.value in ['suspicious', 'malicious']]
            
            if len(threats) > 0:
                if len(alerts) > 0:
                    self.log(f"Created {len(alerts)} alerts from {len(threats)} threats", "PASS")
                else:
                    self.log("No alerts created despite threats", "WARN")
            else:
                self.log("No threats to create alerts from (expected for some test cases)", "INFO")
            
            return True
            
        except Exception as e:
            self.log(f"Alerts creation test failed: {e}", "FAIL")
            import traceback
            traceback.print_exc()
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 70)
        print("E2E Dashboard Demo - Automated Testing")
        print("=" * 70)
        print()
        
        tests = [
            ("Core Detection", self.test_core_detection),
            ("Database Persistence", self.test_database_persistence),
            ("Vector Database", self.test_vector_database),
            ("Metrics Calculation", self.test_metrics_calculation),
            ("Charts Rendering", self.test_charts_rendering),
            ("Alerts Creation", self.test_alerts_creation),
        ]
        
        passed = 0
        failed = 0
        warned = 0
        
        for test_name, test_func in tests:
            print(f"\n[{test_name}]")
            print("-" * 70)
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log(f"Test {test_name} crashed: {e}", "FAIL")
                failed += 1
            time.sleep(0.5)
        
        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Tests Passed: {passed}")
        print(f"Tests Failed: {failed}")
        print(f"Warnings: {warned}")
        print(f"Total Tests: {len(tests)}")
        print()
        
        if failed == 0:
            print("✅ All critical tests passed!")
            print("Dashboard is ready for demo.")
            return 0
        else:
            print(f"❌ {failed} test(s) failed. Please review errors above.")
            return 1
    
    def cleanup(self):
        """Cleanup test database"""
        try:
            self.db.close()
            import os
            if os.path.exists("demo_detections.db"):
                os.remove("demo_detections.db")
            import shutil
            if os.path.exists("chroma_db"):
                shutil.rmtree("chroma_db")
        except:
            pass


def main():
    demo = DashboardDemo()
    try:
        exit_code = demo.run_all_tests()
        return exit_code
    finally:
        demo.cleanup()


if __name__ == '__main__':
    sys.exit(main())

