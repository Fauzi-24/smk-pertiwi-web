from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
from ..config import settings

class RateLimitMiddleware:
    def __init__(self, app):
        self.app = app
        self.request_counts = {}
        self.window_size = settings.rate_limit_window
        self.limit = settings.rate_limit_per_min

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        client_ip = request.client.host
        current_time = time.time()

        # Clean up old records
        self._cleanup(current_time)

        # Check rate limit
        if self._is_rate_limited(client_ip, current_time):
             response = JSONResponse(
                 status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                 content={"detail": "Too many requests. Please try again later."}
             )
             await response(scope, receive, send)
             return

        await self.app(scope, receive, send)

    def _cleanup(self, current_time):
        # Remove entries older than window_size
        to_remove = []
        for ip, data in self.request_counts.items():
            if current_time - data["start_time"] > self.window_size:
                to_remove.append(ip)
        
        for ip in to_remove:
            del self.request_counts[ip]

    def _is_rate_limited(self, client_ip, current_time):
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {
                "count": 1,
                "start_time": current_time
            }
            return False
        
        data = self.request_counts[client_ip]
        if current_time - data["start_time"] > self.window_size:
            # Reset window
            data["count"] = 1
            data["start_time"] = current_time
            return False
        
        data["count"] += 1
        return data["count"] > self.limit
