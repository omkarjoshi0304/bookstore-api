# Bookstore API

A RESTful API for managing a bookstore, built with FastAPI, SQLAlchemy, and JWT authentication.

## Features

- **User Authentication** -- Register, login, and JWT-based session management
- **Role-Based Access** -- Admin users can manage books; regular users can browse
- **Book Management** -- Full CRUD operations with search and genre filtering
- **User Profiles** -- View and update your own account
- **Database Migrations** -- Alembic for schema versioning
- **Containerized** -- Ready to deploy with Docker/Podman

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Auth | JWT (python-jose) + bcrypt |
| Validation | Pydantic v2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Server | Uvicorn |
| Package Manager | uv |

## Project Structure

```
src/bookstore/
├── api/                # Route handlers
│   ├── auth.py         #   POST /register, /login
│   ├── users.py        #   GET/PATCH /users/me
│   ├── books.py        #   CRUD /books
│   └── router.py       #   Aggregates all routes under /api
├── auth/               # Auth utilities
│   ├── jwt.py          #   Token creation & verification
│   └── password.py     #   bcrypt hashing
├── crud/               # Database operations
│   ├── user.py         #   User queries
│   └── book.py         #   Book queries
├── models/             # SQLAlchemy ORM models
│   ├── base.py         #   Base class + TimestampMixin
│   ├── user.py         #   User table
│   └── book.py         #   Book table
├── schemas/            # Pydantic request/response schemas
│   ├── user.py         #   UserCreate, UserResponse, Token
│   └── book.py         #   BookCreate, BookResponse, BookListResponse
├── config.py           # Settings from environment variables
├── database.py         # Engine, session factory, get_db dependency
├── dependencies.py     # get_current_user, get_admin_user
├── exceptions.py       # HTTP exception classes
├── middleware.py       # CORS and request logging
└── main.py             # FastAPI app factory
```

## Getting Started

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd bookstore-api

# Install dependencies
uv sync --dev

# Set up environment variables
cp .env.example .env
# Edit .env with your values (defaults work for local dev with SQLite)
```

### Run the Server

```bash
uv run python main.py
```

The API starts at **http://localhost:8000**. Interactive docs are at **http://localhost:8000/docs**.

### Run Database Migrations

```bash
# Generate a new migration after model changes
uv run python -m alembic revision --autogenerate -m "describe changes"

# Apply migrations
uv run python -m alembic upgrade head
```

### Run Tests

```bash
uv run python -m pytest tests/ -v
```

Tests use an in-memory SQLite database -- no external setup needed.

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Create a new account | None |
| POST | `/api/auth/login` | Get an access token | None |

### Users

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/users/me` | Get your profile | Bearer token |
| PATCH | `/api/users/me` | Update your profile | Bearer token |

### Books

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/books` | List books (search, filter by genre) | None |
| GET | `/api/books/{id}` | Get a single book | None |
| POST | `/api/books` | Add a new book | Admin only |
| PATCH | `/api/books/{id}` | Update a book | Admin only |
| DELETE | `/api/books/{id}` | Delete a book | Admin only |

### Query Parameters for `GET /api/books`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Pagination offset |
| `limit` | int | 20 | Page size (max 100) |
| `search` | string | -- | Search by title or author |
| `genre` | string | -- | Filter by exact genre |

## Usage Examples

### Register a user

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "username": "alice",
    "password": "securepass123",
    "full_name": "Alice Smith"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -d "username=alice@example.com&password=securepass123"
```

Returns:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Browse books

```bash
# List all books
curl http://localhost:8000/api/books

# Search by title or author
curl "http://localhost:8000/api/books?search=gatsby"

# Filter by genre
curl "http://localhost:8000/api/books?genre=Fiction"
```

### Add a book (admin only)

```bash
curl -X POST http://localhost:8000/api/books \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "price": 12.99,
    "description": "A classic novel of the Jazz Age",
    "stock": 25,
    "genre": "Fiction"
  }'
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./bookstore.db` | Database connection string |
| `SECRET_KEY` | `CHANGE-ME-IN-PRODUCTION` | JWT signing key |
| `DEBUG` | `false` | Enable debug mode and SQL logging |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token lifetime |
| `ALLOWED_ORIGINS` | `["http://localhost:3000"]` | CORS allowed origins (JSON array) |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |

## Docker Deployment

### Using Docker Compose (PostgreSQL + API)

```bash
docker compose up --build
```

This starts:
- **PostgreSQL 17** on port 5432
- **Bookstore API** on port 8000

### Standalone Container

```bash
docker build -f Containerfile -t bookstore-api .
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./bookstore.db \
  -e SECRET_KEY=your-secret-key \
  bookstore-api
```

## Making a User an Admin

There is no admin registration endpoint by design. To promote a user to admin, update the database directly:

```sql
UPDATE users SET is_admin = true WHERE email = 'alice@example.com';
```

Or via SQLite CLI for local dev:

```bash
sqlite3 bookstore.db "UPDATE users SET is_admin = 1 WHERE email = 'alice@example.com';"
```

## License

MIT
