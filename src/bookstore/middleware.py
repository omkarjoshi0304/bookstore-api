import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from bookstore.config import get_settings

logger = logging.getLogger("bookstore")


def setup_middleware(app: FastAPI) -> None:
    settings = get_settings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        logger.info(
            "%s %s %d (%.3fs)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
        )
        return response
