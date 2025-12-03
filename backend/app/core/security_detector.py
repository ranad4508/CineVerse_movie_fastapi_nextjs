from datetime import datetime, timedelta
from collections import defaultdict
import re
from typing import Optional, Tuple
from fastapi import Request
from user_agents import parse


class BotDetector:
    BOT_KEYWORDS = [
        'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget',
        'python', 'java', 'perl', 'ruby', 'go-http-client',
        'postman', 'insomnia', 'Thunder', 'httpclient'
    ]
    
    SUSPICIOUS_USER_AGENTS = [
        'sqlmap', 'nikto', 'nmap', 'masscan', 'metasploit',
        'acunetix', 'nessus', 'openvas', 'w3af', 'havij'
    ]
    
    @staticmethod
    def is_bot(user_agent: str) -> bool:
        if not user_agent:
            return True
        
        ua_lower = user_agent.lower()
        
        for keyword in BotDetector.BOT_KEYWORDS:
            if keyword in ua_lower:
                return True
        
        for suspicious in BotDetector.SUSPICIOUS_USER_AGENTS:
            if suspicious in ua_lower:
                return True
        
        try:
            parsed_ua = parse(user_agent)
            if parsed_ua.is_bot:
                return True
        except:
            pass
        
        return False


class SpamDetector:
    def __init__(self):
        self.request_history = defaultdict(list)
        self.spam_scores = defaultdict(float)
        self.blocked_ips = set()
        self.cleanup_interval = timedelta(hours=1)
        self.last_cleanup = datetime.now()
    
    def _cleanup_old_entries(self):
        now = datetime.now()
        if now - self.last_cleanup > self.cleanup_interval:
            cutoff_time = now - timedelta(hours=1)
            for ip in list(self.request_history.keys()):
                self.request_history[ip] = [
                    req_time for req_time in self.request_history[ip]
                    if req_time > cutoff_time
                ]
                if not self.request_history[ip]:
                    del self.request_history[ip]
                    if ip in self.spam_scores:
                        self.spam_scores[ip] *= 0.9
            self.last_cleanup = now
    
    def detect_spam(self, request: Request, user_id: Optional[int] = None) -> Tuple[bool, float]:
        self._cleanup_old_entries()
        
        client_ip = request.client.host if request.client else "unknown"
        now = datetime.now()
        
        if client_ip in self.blocked_ips:
            return True, 100.0
        
        self.request_history[client_ip].append(now)
        spam_score = 0.0
        
        requests_last_minute = [
            req_time for req_time in self.request_history[client_ip]
            if req_time > now - timedelta(minutes=1)
        ]
        if len(requests_last_minute) > 30:
            spam_score += 40.0
        elif len(requests_last_minute) > 15:
            spam_score += 20.0
        
        requests_last_hour = [
            req_time for req_time in self.request_history[client_ip]
            if req_time > now - timedelta(hours=1)
        ]
        if len(requests_last_hour) > 500:
            spam_score += 30.0
        elif len(requests_last_hour) > 200:
            spam_score += 15.0
        
        user_agent = request.headers.get("user-agent", "")
        if BotDetector.is_bot(user_agent):
            spam_score += 25.0
        
        if self._has_sql_injection_attempt(request):
            spam_score += 50.0
        
        if self._has_xss_attempt(request):
            spam_score += 40.0
        
        if self._has_path_traversal_attempt(request):
            spam_score += 45.0
        
        self.spam_scores[client_ip] = spam_score
        
        if spam_score >= 80.0:
            self.blocked_ips.add(client_ip)
            return True, spam_score
        
        return spam_score >= 60.0, spam_score
    
    @staticmethod
    def _has_sql_injection_attempt(request: Request) -> bool:
        sql_patterns = [
            r"('.*?or.*?')",
            r"(union.*?select)",
            r"(select.*?from)",
            r"(insert.*?into)",
            r"(delete.*?from)",
            r"(drop.*?table)",
            r"(update.*?set)",
            r"(declare.*?)",
            r"(execute.*?)",
        ]
        
        query_string = request.url.query
        for pattern in sql_patterns:
            if re.search(pattern, query_string, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def _has_xss_attempt(request: Request) -> bool:
        xss_patterns = [
            r"<script[^>]*>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe",
            r"<img[^>]*on",
        ]
        
        query_string = request.url.query
        for pattern in xss_patterns:
            if re.search(pattern, query_string, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def _has_path_traversal_attempt(request: Request) -> bool:
        path_traversal_patterns = [
            r"\.\./",
            r"\.\.\\",
            r"%2e%2e/",
            r"%2e%2e\\",
        ]
        
        url_path = request.url.path
        for pattern in path_traversal_patterns:
            if re.search(pattern, url_path, re.IGNORECASE):
                return True
        
        return False


spam_detector = SpamDetector()
