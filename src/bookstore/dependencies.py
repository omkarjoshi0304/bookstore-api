from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from bookstore.auth.jwt import decode_access_token
from bookstore.crud.user import get_user_by_id
from bookstore.database import get_db
from bookstore.exceptions import AuthenticationError, ForbiddenError
from bookstore.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    user_id = decode_access_token(token)
    if user_id is None:
        raise AuthenticationError()
    user = get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise AuthenticationError()
    return user


def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise ForbiddenError()
    return user
