import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from bookstore.database import get_db
from bookstore.main import app
from bookstore.models import Base


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
    })
    return response.json()


@pytest.fixture
def auth_headers(client, test_user):
    response = client.post("/api/auth/login", data={
        "username": "test@example.com",
        "password": "testpass123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_user(client, db):
    from bookstore.models.user import User
    from bookstore.auth.password import hash_password

    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=hash_password("adminpass123"),
        full_name="Admin User",
        is_admin=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.post("/api/auth/login", data={
        "username": "admin@example.com",
        "password": "adminpass123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
