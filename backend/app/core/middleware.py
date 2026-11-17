import time
from typing import Dict, List
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from app.core.config import settings


class InMemoryRateLimiter:
    """Sliding-window rate limiter per client IP address."""

    def __init__(self, limit_per_minute: int = 60):
        self.limit = limit_per_minute
        self.clients: Dict[str, List[float]] = {}

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        window_start = now - 60.0

        timestamps = self.clients.get(client_ip, [])
        # Filter out timestamps older than 60 seconds
        recent = [t for t in timestamps if t > window_start]

        if len(recent) >= self.limit:
            self.clients[client_ip] = recent
            return False

        recent.append(now)
        self.clients[client_ip] = recent
        return True


rate_limiter = InMemoryRateLimiter(limit_per_minute=settings.RATE_LIMIT_PER_MINUTE)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude documentation and health check endpoints
        path = request.url.path
        if (
            path in ["/health", "/docs", "/openapi.json", "/redoc"]
            or path.startswith("/static")
            or settings.ENVIRONMENT == "test"
        ):
            return await call_next(request)

        # Get client IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "127.0.0.1"

        if not rate_limiter.is_allowed(client_ip):
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Please wait a minute before making more requests.",
                    "limit_per_minute": rate_limiter.limit,
                },
                headers={"Retry-After": "60"}
            )

        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Apply robust security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

        return response
