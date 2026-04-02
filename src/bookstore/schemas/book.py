from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=10, max_length=13)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    description: str | None = None
    stock: int = Field(default=0, ge=0)
    genre: str | None = Field(None, max_length=100)


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    author: str | None = Field(None, min_length=1, max_length=255)
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    description: str | None = None
    stock: int | None = Field(None, ge=0)
    genre: str | None = Field(None, max_length=100)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    price: Decimal
    description: str | None
    stock: int
    genre: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BookListResponse(BaseModel):
    books: list[BookResponse]
    total: int
