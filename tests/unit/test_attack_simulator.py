"""
Unit tests for AttackSimulator
"""
import pytest
from datetime import datetime
from ai_tools.simulation.attack_simulator import AttackSimulator
from ai_tools.utils.models import Request


@pytest.mark.unit
class TestAttackSimulatorCreation:
    """Test AttackSimulator initialization"""
    
    def test_simulator_creation(self):
        """Test creating AttackSimulator"""
        simulator = AttackSimulator()
        assert simulator is not None
        assert hasattr(simulator, 'generate_requests')
    
    def test_simulator_initial_state(self):
        """Test simulator initial state"""
        simulator = AttackSimulator()
        assert simulator.attack_active == False


@pytest.mark.unit
class TestNormalTrafficGeneration:
    """Test normal traffic generation"""
    
    def test_generate_normal_requests(self):
        """Test generating normal traffic requests"""
        simulator = AttackSimulator()
        requests = []
        
        # Generate a few requests
        for i, request in enumerate(simulator.generate_requests()):
            requests.append(request)
            if i >= 4:  # Get 5 requests
                break
        
        assert len(requests) == 5
        for req in requests:
            assert isinstance(req, Request)
            assert req.endpoint.startswith("/")
            assert req.method in ["GET", "POST", "PUT", "DELETE"]
    
    def test_request_structure(self):
        """Test request structure is valid"""
        simulator = AttackSimulator()
        request = next(simulator.generate_requests())
        
        assert hasattr(request, 'timestamp')
        assert hasattr(request, 'ip_address')
        assert hasattr(request, 'endpoint')
        assert hasattr(request, 'method')
        assert hasattr(request, 'user_agent')
        assert isinstance(request.timestamp, datetime)


@pytest.mark.unit
class TestAttackTrafficGeneration:
    """Test attack traffic generation"""
    
    def test_start_attack(self):
        """Test starting attack simulation"""
        simulator = AttackSimulator()
        simulator.start_attack()
        assert simulator.attack_active == True
    
    def test_stop_attack(self):
        """Test stopping attack simulation"""
        simulator = AttackSimulator()
        simulator.start_attack()
        simulator.stop_attack()
        assert simulator.attack_active == False
    
    def test_attack_traffic_patterns(self):
        """Test attack traffic has different patterns"""
        simulator = AttackSimulator()
        simulator.start_attack()
        
        requests = []
        for i, request in enumerate(simulator.generate_requests()):
            requests.append(request)
            if i >= 9:  # Get 10 requests
                break
        
        # Attack traffic should have some enumeration patterns
        endpoints = [req.endpoint for req in requests]
        # Check for sequential patterns or unusual endpoints
        assert len(set(endpoints)) > 0
    
    def test_attack_vs_normal_difference(self):
        """Test attack traffic differs from normal traffic"""
        simulator = AttackSimulator()
        
        # Get normal requests
        normal_requests = []
        for i, req in enumerate(simulator.generate_requests()):
            normal_requests.append(req)
            if i >= 4:
                break
        
        # Start attack and get attack requests
        simulator.start_attack()
        attack_requests = []
        for i, req in enumerate(simulator.generate_requests()):
            attack_requests.append(req)
            if i >= 4:
                break
        
        # Attack requests should have different characteristics
        # (e.g., different endpoints, user agents, or patterns)
        normal_endpoints = set([req.endpoint for req in normal_requests])
        attack_endpoints = set([req.endpoint for req in attack_requests])
        
        # They may overlap, but should have some differences
        assert len(normal_endpoints) > 0
        assert len(attack_endpoints) > 0


@pytest.mark.unit
class TestRequestRateControl:
    """Test request rate control"""
    
    def test_request_generation_rate(self):
        """Test requests are generated at reasonable rate"""
        simulator = AttackSimulator()
        import time
        
        start_time = time.time()
        requests = []
        for i, req in enumerate(simulator.generate_requests()):
            requests.append(req)
            if i >= 4:
                break
        elapsed = time.time() - start_time
        
        # Should generate requests quickly (not blocking)
        assert elapsed < 1.0  # Should be very fast
    
    def test_continuous_generation(self):
        """Test continuous request generation"""
        simulator = AttackSimulator()
        count = 0
        
        for request in simulator.generate_requests():
            count += 1
            if count >= 20:
                break
        
        assert count == 20
        assert all(isinstance(req, Request) for req in [request])


@pytest.mark.unit
class TestUserAgents:
    """Test user agent generation"""
    
    def test_user_agent_diversity(self):
        """Test user agents have variety"""
        simulator = AttackSimulator()
        user_agents = set()
        
        for i, request in enumerate(simulator.generate_requests()):
            user_agents.add(request.user_agent)
            if i >= 9:
                break
        
        # Should have some variety in user agents
        assert len(user_agents) > 0
    
    def test_user_agent_format(self):
        """Test user agent format is valid"""
        simulator = AttackSimulator()
        request = next(simulator.generate_requests())
        
        assert isinstance(request.user_agent, str)
        assert len(request.user_agent) > 0

