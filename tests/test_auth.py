import pytest


def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"email": "newuser@example.com", "password": "validpass123"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "validpass123"}
    )

    response = client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "anotherpass456"}
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={"email": "notanemail", "password": "validpass123"}
    )

    assert response.status_code == 422


def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={"email": "newuser@example.com", "password": "short"}
    )

    assert response.status_code == 422
                                        
def test_login_success(client):
    # Step 1: First, register a user (we need someone to log in!)
    client.post(
        "/auth/register",
        json={"email": "loginuser@example.com", "password": "validpass123"}
    )

    # Step 2: Now try to log in with the same credentials
    response = client.post(
        "/auth/login",
        json={"email": "loginuser@example.com", "password": "validpass123"}
    )

    # Step 3: Check that login worked
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data          # We got a token back
    assert data["token_type"] == "bearer"  # Token type is "bearer" (industry standard)
    assert len(data["access_token"]) > 50  # JWT tokens are long strings, not short garbage


def test_login_wrong_password(client):
    # Register with one password...
    client.post(
        "/auth/register",
        json={"email": "loginuser@example.com", "password": "correctpass123"}
    )

    # ...but try to log in with a DIFFERENT password
    response = client.post(
        "/auth/login",
        json={"email": "loginuser@example.com", "password": "wrongpass456"}
    )

    # Should be rejected! 401 = "Unauthorized"
    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    # Try to log in as someone who never registered
    response = client.post(
        "/auth/login",
        json={"email": "doesnotexist@example.com", "password": "anypass123"}
    )

    # Should also be 401 — and notice the SAME error message as wrong password!
    # This is intentional security: we don't want hackers to know whether
    # an email exists in our system or not
    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()



def test_get_me_authenticated(client):
    # Register a new user
    client.post(
        "/auth/register",
        json={"email": "meuser@example.com", "password": "validpass123"}
    )

    # Log in to get a token
    login_response = client.post(
        "/auth/login",
        json={"email": "meuser@example.com", "password": "validpass123"}
    )
    token = login_response.json()["access_token"]

    # Use the token to access the protected /me endpoint
    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "meuser@example.com"
    assert "id" in data


def test_get_me_no_token(client):
    # Try to access /me without any token
    response = client.get("/me")

    assert response.status_code == 401


def test_get_me_invalid_token(client):
    # Try with a completely fake token
    response = client.get(
        "/me",
        headers={"Authorization": "Bearer invalidtoken123"}
    )

    assert response.status_code == 401