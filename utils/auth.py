import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def get_auth_token():
    """Login and return the access token"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        }
    )
    token = response.json()["data"]["access_token"]
    return token


def get_headers():
    """Return authorization headers with token"""
    token = get_auth_token()
    return {
        "Authorization": f"Bearer {token}",
        "X-Platform": "web"
    }