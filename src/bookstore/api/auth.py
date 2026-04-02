from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from bookstore.auth.jwt import create_access_token
from bookstore.crud.user import authenticate_user, create_user, get_user_by_email, get_user_by_username
from bookstore.database import get_db
from bookstore.exceptions import AuthenticationError, DuplicateError
from bookstore.schemas.user import Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, data.email):
        raise DuplicateError("Email already registered")
    if get_user_by_username(db, data.username):
        raise DuplicateError("Username already taken")
    return create_user(db, data)


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form.username, form.password)
    if user is None:
        raise AuthenticationError()
    return Token(access_token=create_access_token(user.id))
