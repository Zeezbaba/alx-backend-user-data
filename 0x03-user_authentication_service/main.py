#!/usr/bin/env python3
"""Integration test
"""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration."""
    response = requests.post(f"{BASE_URL}/users",
                             data={"email": email,
                                   "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email,
                               "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email,
                                   "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login with correct password and return session ID."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email,
                                   "password": password})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["message"] == "logged in"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test accessing profile without login."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test accessing profile with login."""
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """Test logging out."""
    response = requests.delete(f"{BASE_URL}/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Test requesting a password reset token."""
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    return data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating the password."""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token,
              "new_password": new_password},
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
