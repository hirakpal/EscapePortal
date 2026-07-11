from datetime import datetime, timedelta
import time

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold  # Max failures before opening
        self.recovery_timeout = recovery_timeout    # Seconds to wait before retry
        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "OPEN":
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.recovery_timeout):
                self.state = "HALF_OPEN"  # Try again
            else:
                return {"error": "Service temporarily unavailable. Please try again later."}
        
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            self.state = "CLOSED"
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = datetime.now()
            
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
            
            raise e  # Let safe_execute handle the error message

# Global instance
circuit_breaker = CircuitBreaker()
