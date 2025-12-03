from fastapi import Request, HTTPException, status, Depends
from typing import Callable, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import threading


class ThrottleManager:
    def __init__(self):
        self.request_counts = defaultdict(lambda: {'timestamps': []})
        self.lock = threading.Lock()
    
    def is_throttled(
        self,
        identifier: str,
        limit: int = 100,
        window_seconds: int = 60
    ) -> bool:
        with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=window_seconds)
            
            self.request_counts[identifier]['timestamps'] = [
                ts for ts in self.request_counts[identifier]['timestamps']
                if ts > cutoff
            ]
            
            if len(self.request_counts[identifier]['timestamps']) >= limit:
                return True
            
            self.request_counts[identifier]['timestamps'].append(now)
            return False
    
    def cleanup_old_entries(self, max_age_hours: int = 2):
        with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(hours=max_age_hours)
            
            expired_identifiers = []
            for identifier, data in self.request_counts.items():
                data['timestamps'] = [
                    ts for ts in data['timestamps']
                    if ts > cutoff
                ]
                if not data['timestamps']:
                    expired_identifiers.append(identifier)
            
            for identifier in expired_identifiers:
                del self.request_counts[identifier]


throttle_manager = ThrottleManager()


def get_rate_limit_key(calls: int, period: int):
    async def check_rate_limit(request: Request):
        identifier = request.client.host if request.client else "unknown"
        
        is_throttled = throttle_manager.is_throttled(
            identifier=identifier,
            limit=calls,
            window_seconds=period
        )
        
        if is_throttled:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {calls} requests per {period} seconds"
            )
        
        return identifier
    
    return check_rate_limit


RATE_LIMITS = {
    "auth_register": {"calls": 5, "period": 3600},
    "auth_login": {"calls": 10, "period": 900},
    "auth_verify": {"calls": 10, "period": 300},
    "search": {"calls": 30, "period": 60},
    "bookings": {"calls": 20, "period": 60},
    "public": {"calls": 100, "period": 60},
}
