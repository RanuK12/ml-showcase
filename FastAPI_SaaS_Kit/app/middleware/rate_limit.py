import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

# Simple in-memory rate limiter. For production, swap with Redis-based.
_requests: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT = 60  # requests per window
WINDOW = 60  # seconds


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        _requests[client_ip] = [t for t in _requests[client_ip] if now - t < WINDOW]
        if len(_requests[client_ip]) >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        _requests[client_ip].append(now)
        return await call_next(request)
