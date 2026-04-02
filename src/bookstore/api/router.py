from fastapi import APIRouter

from bookstore.api.auth import router as auth_router
from bookstore.api.books import router as books_router
from bookstore.api.users import router as users_router

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(books_router)
