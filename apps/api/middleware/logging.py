# Auto-generated file
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from core.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"{request.method} { request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {duration}ms"

        )

        return response