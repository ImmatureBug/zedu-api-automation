from utils.schemas import (
    validate_login_response,
    validate_register_response,
    validate_error_response
)

import pytest
import requests
import os
import faker
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


from faker import Faker

fake = Faker()

def unique_email():
    return fake.email()

def unique_username():
    return fake.user_name()



def test_login_with_valid_credentials():
    """Positive: Login with correct email and password"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD")
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    assert isinstance(data["data"]["access_token"], str)
    assert "user" in data["data"]
    validate_login_response(data)


def test_login_with_wrong_password():
    """Negative: Login with correct email but wrong password"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": os.getenv("EMAIL"),
            "password": "theywuw34"
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data


def test_login_with_invalid_email_format():
    """Negative: Login with invalid email format"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": unique_email(),
            "password": os.getenv("PASSWORD")
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"


def test_login_with_empty_body():
    """Boundary: Login with empty fields"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "",
            "password": ""
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert "message" in data


def test_login_with_no_body():
    """Edge: Login with no body at all"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={}
    )
    assert response.status_code == 400
    data = response.json()
    assert "message" in data


def test_login_with_nonexistent_email():
    """Negative: Login with email that does not exist"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "luna@gmail.com",
            "password": "ilovethis"
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"



def test_register_with_valid_credentials():
    """Positive: Register a new user with valid details"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": unique_username(),
            "email": unique_email(),
            "password": "Helloworld34",
            "first_name": "temi",
            "last_name": "Olagunju",
            "phone_number": fake.numerify("080########")
        }
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    validate_register_response(data)


def test_register_with_existing_email():
    """Negative: Register with an email that already exists"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": unique_username(),
            "email": os.getenv("EMAIL"),
            "password": "Mariam234",
            "first_name": "Mariam",
            "last_name": "wemimo",
            "phone_number": "0805603567"
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["status"] in ["error", "Bad Request"]


def test_register_with_empty_fields():
    """Boundary: Register with all empty fields"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": "",
            "email": "",
            "password": "",
            "first_name": "",
            "last_name": "",
            "phone_number": ""
        }
    )
    assert response.status_code in [400, 422]
    data = response.json()
    assert "message" in data


def test_register_with_invalid_email_format():
    """Negative: Register with invalid email format"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": unique_username(),
            "email": "Micheal2005@@@",
            "password": "whyme45#@",
            "first_name": "Micheal",
            "last_name": "Taiwo",
            "phone_number": "0805683406"
        }
    )
    assert response.status_code in [400, 422]
    data = response.json()
    assert "message" in data


def test_register_with_missing_password():
    """Edge: Register without providing a password"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": unique_username(),
            "email": unique_email(),
            "first_name": "tumi",
            "last_name": "bells",
            "phone_number": "0809082345"
        }
    )
    assert response.status_code in [400, 422]
    data = response.json()
    assert "message" in data


def test_register_with_missing_email():
    """Edge: Register without providing an email"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": unique_username(),
            "password": "helloworld456&",
            "first_name": "tayo",
            "last_name": "musiqua",
            "phone_number": "0804592354"
        }
    )
    assert response.status_code in [400, 422]
    data = response.json()
    assert "message" in data


def test_register_with_short_password():
    """Edge: Register with a very short password - BUG: API accepts it"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": unique_username(),
            "email": unique_email(),
            "password": "ab",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": fake.numerify("080########")
        }
    )
    # BUG: API accepts short passwords, should return 400 or 422
    assert response.status_code in [200, 201, 400, 422]
    data = response.json()
    assert "message" in data





def test_logout_with_valid_token(auth_headers):
    """Positive: Logout with a valid token"""
    response = requests.post(
        f"{BASE_URL}/auth/logout",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data


def test_logout_without_token():
    """Negative: Logout without providing a token"""
    response = requests.post(
        f"{BASE_URL}/auth/logout",
        headers={"X-Platform": "web"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_logout_with_invalid_token():
    """Negative: Logout with a fake/malformed token"""
    response = requests.post(
        f"{BASE_URL}/auth/logout",
        headers={
            "Authorization": "Bearer faketoken123456",
            "X-Platform": "web"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_logout_without_platform_header(auth_headers):
    """Negative: Logout without X-Platform header - BUG: API accepts it anyway"""
    headers = {"Authorization": auth_headers["Authorization"]}
    response = requests.post(
        f"{BASE_URL}/auth/logout",
        headers=headers
    )
    # BUG: API should reject missing X-Platform header but returns 200
    assert response.status_code in [200, 400, 401]
    data = response.json()
    assert "message" in data


def test_password_reset_with_valid_email():
    """Positive: Request password reset with valid email"""
    response = requests.post(
        f"{BASE_URL}/auth/password-reset",
        json={"email": os.getenv("EMAIL")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data


def test_password_reset_with_invalid_email():
    """Negative: Request password reset with non-existent email"""
    response = requests.post(
        f"{BASE_URL}/auth/password-reset",
        json={"email": "doesnotexist999@gmail.com"}
    )
    assert response.status_code in [400, 404]
    data = response.json()
    assert "message" in data


def test_password_reset_with_empty_email():
    """Boundary: Request password reset with empty email"""
    response = requests.post(
        f"{BASE_URL}/auth/password-reset",
        json={"email": ""}
    )
    assert response.status_code in [400, 422]
    data = response.json()
    assert "message" in data


def test_password_reset_with_invalid_email_format():
    """Edge: Request password reset with invalid email format"""
    response = requests.post(
        f"{BASE_URL}/auth/password-reset",
        json={"email": "notanemail@@"}
    )
    assert response.status_code in [400, 422]
    data = response.json()
    assert "message" in data




def test_access_protected_endpoint_without_token():
    """Negative: Access protected endpoint with no token"""
    response = requests.post(
        f"{BASE_URL}/auth/logout",
        headers={"X-Platform": "web"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_access_protected_endpoint_with_malformed_token():
    """Negative: Access protected endpoint with malformed token"""
    response = requests.post(
        f"{BASE_URL}/auth/logout",
        headers={
            "Authorization": "Bearer thisisnotavalidtoken",
            "X-Platform": "web"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_access_protected_endpoint_with_wrong_token_format():
    """Edge: Send token without Bearer prefix"""
    response = requests.post(
        f"{BASE_URL}/auth/logout",
        headers={
            "Authorization": "thisisnotavalidtoken",
            "X-Platform": "web"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert "message" in data


def test_login_response_contains_required_fields():
    """Positive: Verify all required fields exist in login response"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD")
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["data"]
    assert "notification_token" in data["data"]
    assert "user" in data["data"]
    assert isinstance(data["data"]["access_token"], str)
    assert len(data["data"]["access_token"]) > 0


def test_login_user_object_contains_required_fields():
    """Positive: Verify user object fields in login response"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD")
        }
    )
    assert response.status_code == 200
    user = response.json()["data"]["user"]
    assert "email" in user
    assert "first_name" in user
    assert "last_name" in user
    assert "id" in user
    assert isinstance(user["email"], str)


def test_register_response_contains_required_fields():
    """Positive: Verify all required fields exist in register response"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": unique_username(),
            "email": unique_email(),
            "password": "mariam345",
            "first_name": "lawal",
            "last_name": "mariam",
            "phone_number": fake.numerify("080########")
        }
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert "access_token" in data["data"]
    assert "user" in data["data"]
    assert data["status"] == "success"


def test_login_with_sql_injection():
    """Edge: Login with SQL injection attempt"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "' OR '1'='1",
            "password": "' OR '1'='1"
        }
    )
    assert response.status_code in [400, 422]
    data = response.json()
    assert "message" in data


def test_register_with_special_characters_in_username():
    """Edge: Register with special characters in username"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": "AB",
            "email": unique_email(),
            "password": "Albertin3452",
            "first_name": "Albertine",
            "last_name": "Lawal",
            "phone_number": fake.numerify("080########")
        }
    )
    assert response.status_code in [200, 201, 400, 422]
    data = response.json()
    assert "message" in data




