from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from bookstore.crud.user import get_user_by_email, get_user_by_username, update_user
from bookstore.database import get_db
from bookstore.dependencies import get_current_user
from bookstore.exceptions import DuplicateError
from bookstore.models.user import User
from bookstore.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def read_current_user(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserResponse)
def update_current_user(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.email and data.email != user.email and get_user_by_email(db, data.email):
        raise DuplicateError("Email already registered")
    if data.username and data.username != user.username and get_user_by_username(db, data.username):
        raise DuplicateError("Username already taken")
    return update_user(db, user, data)
