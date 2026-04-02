from contextlib import asynccontextmanager

from fastapi import FastAPI

from bookstore.api.router import api_router
from bookstore.config import get_settings
from bookstore.database import engine
from bookstore.models import Base
from bookstore.middleware import setup_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    setup_middleware(app)
    app.include_router(api_router)
    return app


app = create_app()
