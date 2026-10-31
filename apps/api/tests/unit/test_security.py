from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
    decode_access_token,
)


def test_password_hash_round_trip():
    password = "a-strong-test-password-123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_token_round_trip():
    token = create_access_token("test-user")
    assert decode_access_token(token)["sub"] == "test-user"
