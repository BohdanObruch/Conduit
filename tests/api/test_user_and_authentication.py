from demo_apps_project_tests.data.fake_data import email, password, username, bio, picture
from schemas.conduit import *
from pytest_voluptuous import S
from demo_apps_project_tests.utils.sessions import conduit
from allure import tag, title
from tests.conftest import dotenv


user_email = dotenv.get('EMAIL')
user_password = dotenv.get('PASSWORD')


@tag('API')
@title("Login for existing user")
def test_login_for_existing_user():
    data = {
        "user": {
            "email": user_email,
            "password": user_password
        }
    }
    response = conduit().post('/users/login',
                              json=data
                              )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == user_email
    assert S(user) == response.json()


@tag('API')
@title("Gets the currently logged-in user")
def test_get_current_user(user_authorization):
    token = user_authorization[0]
    registered_user_email = user_authorization[1]
    headers = {
        'Authorization': f'Token {token}'

    }
    response = conduit().get('/user',
                             headers=headers
                             )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == registered_user_email
    assert S(user) == response.json()


@tag('API')
@title("Updated user information for current user")
def test_update_current_user(register_user):
    token = register_user[0]
    headers = {
        'Authorization': f'Token {token}'
    }
    data = {
        "user": {
            "email": email,
            "password": password,
            "username": username,
            "bio": bio,
            "image": picture
        }
    }
    response = conduit().put('/user',
                             headers=headers,
                             json=data
                             )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == email
    assert response.json()["user"]["username"] == username
    assert response.json()["user"]["bio"] == bio
    assert response.json()["user"]["image"] == picture
    assert S(user) == response.json()
