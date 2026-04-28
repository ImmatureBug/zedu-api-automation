import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


def test_get_current_user_with_valid_token(auth_headers):
    """Positive: Get current user with valid token"""
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "user" in data["data"]
    assert "email" in data["data"]["user"]
    assert isinstance(data["data"]["user"]["email"], str)


def test_get_current_user_without_token():
    """Negative: Get current user without token"""
    response = requests.get(
        f"{BASE_URL}/users/me"
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_get_current_user_with_invalid_token():
    """Negative: Get current user with fake token"""
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers={
            "Authorization": "Bearer faketoken123",
            "X-Platform": "web"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_get_all_users_with_valid_token(auth_headers):
    """Positive: Get all users with valid token"""
    response = requests.get(
        f"{BASE_URL}/users",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


def test_get_all_users_without_token():
    """Negative: Get all users without token"""
    response = requests.get(
        f"{BASE_URL}/users"
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_get_all_users_with_malformed_token():
    """Negative: Get all users with malformed token"""
    response = requests.get(
        f"{BASE_URL}/users",
        headers={
            "Authorization": "Bearer thisisafaketoken",
            "X-Platform": "web"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_get_user_with_invalid_id(auth_headers):
    """Negative: Get user with non-existent ID"""
    response = requests.get(
        f"{BASE_URL}/users/00000000-0000-0000-0000-000000000000",
        headers=auth_headers
    )
    assert response.status_code in [400, 404]
    data = response.json()
    assert "message" in data


def test_get_user_with_invalid_uuid_format(auth_headers):
    """Edge: Get user with invalid UUID format"""
    response = requests.get(
        f"{BASE_URL}/users/notauuid",
        headers=auth_headers
    )
    assert response.status_code in [400, 404]
    data = response.json()
    assert "message" in data


def test_get_user_without_token():
    """Negative: Get specific user without token"""
    response = requests.get(
        f"{BASE_URL}/users/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data
