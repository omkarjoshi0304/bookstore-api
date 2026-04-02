from sqlalchemy import func, select
from sqlalchemy.orm import Session

from bookstore.models.book import Book
from bookstore.schemas.book import BookCreate, BookUpdate


def get_book_by_id(db: Session, book_id: int) -> Book | None:
    return db.get(Book, book_id)


def get_book_by_isbn(db: Session, isbn: str) -> Book | None:
    return db.scalars(select(Book).where(Book.isbn == isbn)).first()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
    genre: str | None = None,
) -> tuple[list[Book], int]:
    query = select(Book)
    count_query = select(func.count()).select_from(Book)

    if search:
        pattern = f"%{search}%"
        filter_clause = Book.title.ilike(pattern) | Book.author.ilike(pattern)
        query = query.where(filter_clause)
        count_query = count_query.where(filter_clause)

    if genre:
        query = query.where(Book.genre == genre)
        count_query = count_query.where(Book.genre == genre)

    total = db.scalar(count_query) or 0
    books = list(db.scalars(query.offset(skip).limit(limit)).all())
    return books, total


def create_book(db: Session, data: BookCreate) -> Book:
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book: Book, data: BookUpdate) -> Book:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
