import uvicorn

from bookstore.config import get_settings


def main():
    settings = get_settings()
    uvicorn.run(
        "bookstore.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
