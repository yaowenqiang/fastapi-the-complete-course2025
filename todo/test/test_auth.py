from .utils import *
from starlette import status

from ..routers.auth import get_db,authenticate_user, create_access_token,get_current_user, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import  HTTPException

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, '123456', db)
    assert authenticated_user is not None
    assert test_user.username == authenticated_user.username
    assert test_user.hashed_password == authenticated_user.hashed_password

    non_exist_user = authenticate_user('WrongUserName', '123456', db)
    assert non_exist_user is False

    wrong_password_user = authenticate_user(test_user.username, '1234567', db)
    assert wrong_password_user is False

def test_create_access_token(test_user):
    username = test_user.username
    user_id = 1
    role = 'user'
    expire_delta = timedelta(1)
    token = create_access_token(username, user_id, role, expire_delta)
    decoded_token = jwt.decode(token, SECRET_KEY,algorithms=ALGORITHM,options={'verify_signature': False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_current_user_valid_token(test_user):
    encode = {
        'sub': 'jacky.yao',
        'id': 1,
        'role': 'admin'
    }

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token)

    assert user == {
        'username': 'jacky.yao',
        'id': 1,
        'role': 'admin'
    }

@pytest.mark.asyncio
async def test_current_user_missing_payload(test_user):
    encode = {
        'role': 'user'
    }

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exit_info:
        await get_current_user(token=token)

    assert exit_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exit_info.value.detail == 'Could not validate user.'
