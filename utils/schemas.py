def validate_login_response(data):
    """Validate login response has required fields and correct types"""
    assert "status" in data
    assert "data" in data
    assert "access_token" in data["data"]
    assert "user" in data["data"]
    assert isinstance(data["data"]["access_token"], str)
    assert len(data["data"]["access_token"]) > 0
    user = data["data"]["user"]
    assert "email" in user
    assert "first_name" in user
    assert "last_name" in user
    assert "id" in user
    assert isinstance(user["email"], str)


def validate_register_response(data):
    """Validate register response has required fields and correct types"""
    assert "status" in data
    assert data["status"] == "success"
    assert "data" in data
    assert "access_token" in data["data"]
    assert "user" in data["data"]
    assert isinstance(data["data"]["access_token"], str)


def validate_error_response(data):
    """Validate error response has required fields"""
    assert "message" in data or "status" in data


def validate_user_profile(data):
    """Validate user profile response"""
    assert "data" in data
    assert "user" in data["data"]
    user = data["data"]["user"]
    assert "email" in user
    assert isinstance(user["email"], str)