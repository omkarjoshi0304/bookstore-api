import pytest

BOOK_DATA = {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "price": 12.99,
    "description": "A classic novel",
    "stock": 10,
    "genre": "Fiction",
}


class TestListBooks:
    def test_list_empty(self, client):
        response = client.get("/api/books")
        assert response.status_code == 200
        data = response.json()
        assert data["books"] == []
        assert data["total"] == 0

    def test_list_with_search(self, client, admin_user):
        client.post("/api/books", json=BOOK_DATA, headers=admin_user)
        response = client.get("/api/books", params={"search": "Gatsby"})
        assert response.json()["total"] == 1

    def test_list_with_genre_filter(self, client, admin_user):
        client.post("/api/books", json=BOOK_DATA, headers=admin_user)
        response = client.get("/api/books", params={"genre": "Fiction"})
        assert response.json()["total"] == 1
        response = client.get("/api/books", params={"genre": "Sci-Fi"})
        assert response.json()["total"] == 0


class TestCreateBook:
    def test_create_as_admin(self, client, admin_user):
        response = client.post("/api/books", json=BOOK_DATA, headers=admin_user)
        assert response.status_code == 201
        assert response.json()["title"] == "The Great Gatsby"

    def test_create_as_regular_user(self, client, auth_headers):
        response = client.post("/api/books", json=BOOK_DATA, headers=auth_headers)
        assert response.status_code == 403

    def test_create_unauthenticated(self, client):
        response = client.post("/api/books", json=BOOK_DATA)
        assert response.status_code == 401

    def test_create_duplicate_isbn(self, client, admin_user):
        client.post("/api/books", json=BOOK_DATA, headers=admin_user)
        response = client.post("/api/books", json=BOOK_DATA, headers=admin_user)
        assert response.status_code == 409


class TestGetBook:
    def test_get_existing(self, client, admin_user):
        create = client.post("/api/books", json=BOOK_DATA, headers=admin_user)
        book_id = create.json()["id"]
        response = client.get(f"/api/books/{book_id}")
        assert response.status_code == 200
        assert response.json()["isbn"] == "9780743273565"

    def test_get_not_found(self, client):
        response = client.get("/api/books/999")
        assert response.status_code == 404


class TestUpdateBook:
    def test_update_as_admin(self, client, admin_user):
        create = client.post("/api/books", json=BOOK_DATA, headers=admin_user)
        book_id = create.json()["id"]
        response = client.patch(
            f"/api/books/{book_id}",
            json={"price": 15.99},
            headers=admin_user,
        )
        assert response.status_code == 200
        assert float(response.json()["price"]) == 15.99


class TestDeleteBook:
    def test_delete_as_admin(self, client, admin_user):
        create = client.post("/api/books", json=BOOK_DATA, headers=admin_user)
        book_id = create.json()["id"]
        response = client.delete(f"/api/books/{book_id}", headers=admin_user)
        assert response.status_code == 204

    def test_delete_not_found(self, client, admin_user):
        response = client.delete("/api/books/999", headers=admin_user)
        assert response.status_code == 404
