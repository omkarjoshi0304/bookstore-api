from sqlalchemy import select
from sqlalchemy.orm import Session

from bookstore.auth.password import hash_password, verify_password
from bookstore.models.user import User
from bookstore.schemas.user import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalars(select(User).where(User.email == email)).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.scalars(select(User).where(User.username == username)).first()


def create_user(db: Session, data: UserCreate) -> User:
    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user
