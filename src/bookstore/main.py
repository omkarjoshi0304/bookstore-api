from fastapi import FastAPI

from bookstore.api.router import api_router
from bookstore.config import get_settings
from bookstore.middleware import setup_middleware


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )
    setup_middleware(app)
    app.include_router(api_router)
    return app


app = create_app()
