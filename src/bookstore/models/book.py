from decimal import Decimal

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from bookstore.models.base import Base, TimestampMixin


class Book(TimestampMixin, Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    isbn: Mapped[str] = mapped_column(String(13), unique=True, nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    stock: Mapped[int] = mapped_column(default=0)
    genre: Mapped[str | None] = mapped_column(String(100))
