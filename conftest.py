import pytest
import os
from dotenv import load_dotenv
from utils.auth import get_auth_token, get_headers

load_dotenv()


@pytest.fixture
def base_url():
    return os.getenv("BASE_URL")


@pytest.fixture
def auth_headers():
    return get_headers()


@pytest.fixture
def auth_token():
    return get_auth_token()