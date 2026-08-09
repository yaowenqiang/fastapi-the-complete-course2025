from starlette import status

from .utils import *
from ..routers.user import get_db, get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is not None

    assert response.json()['username'] == 'jacky.yao'
    assert response.json()['email'] == 'myemail@mydomain.com'
    assert response.json()['first_name'] == 'jacky'
    assert response.json()['last_name'] == 'yao'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '1111'


def test_change_password_success(test_user):
    response = client.put('/user/password',json={
        'password': '123456',
        'new_password': '12345678',
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put('/user/password',json={
        'password': '12345678',
        'new_password': '12345678',
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Error on password change'

def test_change_phone_number_success(test_user):
    phone_number = '12345678'
    response = client.put(f'/user/phonenumber/{phone_number}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
