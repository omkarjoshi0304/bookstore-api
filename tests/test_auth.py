class TestRegister:
    def test_register_success(self, client):
        response = client.post("/api/auth/register", json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "securepass123",
            "full_name": "New User",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["username"] == "newuser"
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client, test_user):
        response = client.post("/api/auth/register", json={
            "email": "test@example.com",
            "username": "another",
            "password": "securepass123",
        })
        assert response.status_code == 409

    def test_register_short_password(self, client):
        response = client.post("/api/auth/register", json={
            "email": "x@example.com",
            "username": "shortpw",
            "password": "short",
        })
        assert response.status_code == 422


class TestLogin:
    def test_login_success(self, client, test_user):
        response = client.post("/api/auth/login", data={
            "username": "test@example.com",
            "password": "testpass123",
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client, test_user):
        response = client.post("/api/auth/login", data={
            "username": "test@example.com",
            "password": "wrongpassword",
        })
        assert response.status_code == 401


class TestCurrentUser:
    def test_get_me(self, client, auth_headers):
        response = client.get("/api/users/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_get_me_unauthenticated(self, client):
        response = client.get("/api/users/me")
        assert response.status_code == 401
