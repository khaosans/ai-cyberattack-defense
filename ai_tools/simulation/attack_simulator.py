"""
Attack Simulator - Generates realistic traffic patterns including GTG-1002 attacks
"""
import random
import time
from datetime import datetime, timedelta
from typing import Generator, Optional
from ..utils.models import Request
from ..config import Config


class AttackSimulator:
    """
    Generates realistic simulated traffic:
    - Normal traffic: Human-like patterns
    - GTG-1002 attack: High-speed systematic enumeration
    - Mixed traffic: Normal with intermittent attacks
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize simulator"""
        self.config = config or Config()
        self.is_attacking = False
        self.attack_start_time: Optional[datetime] = None
        
        # Normal endpoints pool
        self.normal_endpoints = [
            "/api/home",
            "/api/dashboard",
            "/api/profile",
            "/api/settings",
            "/api/products",
            "/api/search",
            "/api/cart",
            "/api/checkout",
            "/api/about",
            "/api/contact"
        ]
        
        # Attack target endpoints (for enumeration)
        self.attack_targets = [
            "/api/user",
            "/api/admin",
            "/api/data",
            "/api/config",
            "/api/system"
        ]
        
        # IP addresses pool
        self.ip_pool = [
            "192.168.1.100",
            "192.168.1.101",
            "10.0.0.50",
            "172.16.0.25",
            "203.0.113.10"
        ]
        
        # Attack IP (simulated attacker)
        self.attack_ip = "198.51.100.42"
        
        # User agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        
        # Attack user agent (simulated AI agent)
        self.attack_user_agent = "Claude-Code-Agent/1.0"
    
    def generate_normal_request(self) -> Request:
        """Generate a normal human-like request"""
        endpoint = random.choice(self.normal_endpoints)
        ip = random.choice(self.ip_pool)
        user_agent = random.choice(self.user_agents)
        method = random.choice(["GET", "POST"])
        
        # Add some randomness to endpoint
        if random.random() < 0.3:
            endpoint += f"?param={random.randint(1, 100)}"
        
        return Request(
            timestamp=datetime.now(),
            ip_address=ip,
            endpoint=endpoint,
            method=method,
            user_agent=user_agent,
            parameters={"param": random.randint(1, 100)} if "?" in endpoint else None
        )
    
    def generate_attack_request(self, sequence_number: int) -> Request:
        """Generate a GTG-1002 style attack request"""
        # Select attack target
        target_base = random.choice(self.attack_targets)
        
        # Systematic enumeration pattern
        endpoint = f"{target_base}/{sequence_number}"
        
        # Sometimes add parameters
        if random.random() < 0.5:
            endpoint += f"?id={sequence_number}"
        
        return Request(
            timestamp=datetime.now(),
            ip_address=self.attack_ip,
            endpoint=endpoint,
            method="GET",
            user_agent=self.attack_user_agent,
            parameters={"id": sequence_number} if "?" in endpoint else None
        )
    
    def start_attack(self):
        """Start attack simulation"""
        self.is_attacking = True
        self.attack_start_time = datetime.now()
    
    def stop_attack(self):
        """Stop attack simulation"""
        self.is_attacking = False
        self.attack_start_time = None
    
    def generate_requests(self, attack_intensity: float = 0.0, no_sleep: bool = False) -> Generator[Request, None, None]:
        """
        Generate continuous stream of requests
        
        Args:
            attack_intensity: Ratio of attack requests (0.0 to 1.0)
            no_sleep: If True, skip sleep delays (for dashboard batch processing)
        
        Yields:
            Request objects
        """
        attack_sequence = 0
        
        while True:
            # Determine if we should generate attack traffic
            if self.is_attacking or random.random() < attack_intensity:
                # Generate high-speed attack requests
                # GTG-1002 style: thousands per second
                requests_per_batch = random.randint(5, 15)
                for _ in range(requests_per_batch):
                    attack_sequence += 1
                    yield self.generate_attack_request(attack_sequence)
                    # Very short delay for attack (simulating superhuman speed)
                    # Skip sleep if no_sleep is True (dashboard handles timing)
                    if not no_sleep:
                        time.sleep(0.01)
            else:
                # Generate normal traffic
                yield self.generate_normal_request()
                # Human-like delay (1-3 seconds) - skip if no_sleep
                if not no_sleep:
                    time.sleep(random.uniform(1.0, 3.0))
    
    def generate_batch(self, count: int, attack_ratio: float = 0.0) -> list[Request]:
        """
        Generate a batch of requests
        
        Args:
            count: Number of requests to generate
            attack_ratio: Ratio of attack requests (0.0 to 1.0)
            
        Returns:
            List of Request objects
        """
        requests = []
        attack_count = int(count * attack_ratio)
        normal_count = count - attack_count
        
        # Generate attack requests
        for i in range(attack_count):
            requests.append(self.generate_attack_request(i + 1))
        
        # Generate normal requests
        for _ in range(normal_count):
            requests.append(self.generate_normal_request())
        
        # Shuffle to mix attack and normal traffic
        random.shuffle(requests)
        
        return requests

