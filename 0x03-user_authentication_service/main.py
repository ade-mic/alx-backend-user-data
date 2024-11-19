#!/usr/bin/env python3
"""
Create a new module called main.py.
Create one function for each of the following tasks.
Use the requests module to query your web server for the
corresponding end-point. Use assert to validate the response’s
expected status code and payload (if any) for each task.
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(f"{BASE_URL}/users",
                             son={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    print("register_user: OK")


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with a wrong password."""
    response = requests.post(f"{BASE_URL}/sessions",
                             json={"email": email, "password": password})
    assert response.status_code == 401
    print("log_in_wrong_password: OK")


def log_in(email: str, password: str) -> str:
    """Log in with the correct password."""
    response = requests.post(f"{BASE_URL}/sessions",
                             json={"email": email, "password": password})
    assert response.status_code == 200
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    print("log_in: OK")
    return session_id


def profile_unlogged() -> None:
    """Try accessing the profile while not logged in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403
    print("profile_unlogged: OK")


def profile_logged(session_id: str) -> None:
    """Access the profile while logged in."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()
    print("profile_logged: OK")


def log_out(session_id: str) -> None:
    """Log out the user."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "logout successful"}
    print("log_out: OK")


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    response = requests.post(f"{BASE_URL}/reset_password",
                             json={"email": email})
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert reset_token is not None
    print("reset_password_token: OK")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password using the reset token."""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        json={"email": email, "reset_token": reset_token,
              "new_password": new_password}
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "password updated"}
    print("update_password: OK")


# Test Script
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
