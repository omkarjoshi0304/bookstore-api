from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from bookstore.crud.book import create_book, delete_book, get_book_by_id, get_book_by_isbn, get_books, update_book
from bookstore.database import get_db
from bookstore.dependencies import get_admin_user, get_current_user
from bookstore.exceptions import DuplicateError, NotFoundError
from bookstore.models.user import User
from bookstore.schemas.book import BookCreate, BookListResponse, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=BookListResponse)
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = None,
    genre: str | None = None,
    db: Session = Depends(get_db),
):
    books, total = get_books(db, skip=skip, limit=limit, search=search, genre=genre)
    return BookListResponse(books=books, total=total)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)
    if book is None:
        raise NotFoundError("Book not found")
    return book


@router.post("", response_model=BookResponse, status_code=201)
def add_book(
    data: BookCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    if get_book_by_isbn(db, data.isbn):
        raise DuplicateError("Book with this ISBN already exists")
    return create_book(db, data)


@router.patch("/{book_id}", response_model=BookResponse)
def edit_book(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    book = get_book_by_id(db, book_id)
    if book is None:
        raise NotFoundError("Book not found")
    return update_book(db, book, data)


@router.delete("/{book_id}", status_code=204)
def remove_book(
    book_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_admin_user),
):
    book = get_book_by_id(db, book_id)
    if book is None:
        raise NotFoundError("Book not found")
    delete_book(db, book)
