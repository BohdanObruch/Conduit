from demo_apps_project_tests.model.authorization import user_authorization
from schemas.conduit import *
from pytest_voluptuous import S
from demo_apps_project_tests.utils.sessions import conduit
from allure import tag, title
from tests.conftest import dotenv

user_name = dotenv.get('USERNAME_API')


@tag('API')
@title("Get a profile of a user of the system")
def test_get_a_profile_of_a_user_of_the_system():
    user_data = user_authorization()
    username = user_data["username"]
    response = conduit().get(f'/profiles/{username}')
    assert response.status_code == 200
    assert response.json()["profile"]["username"] == username
    assert S(profile) == response.json()


@tag('API')
@title("Follow a user by username")
def test_follow_a_user_by_username():
    user_data = user_authorization()
    token = user_data["token"]
    headers = {
        'Authorization': f'Token {token}'

    }
    response = conduit().post(f'/profiles/{user_name}/follow',
                              headers=headers)
    assert response.status_code == 200
    assert response.json()["profile"]["username"] == user_name
    assert response.json()["profile"]["following"] is True
    assert S(profile) == response.json()


@tag('API')
@title("Unfollow a user by username")
def test_unfollow_a_user_by_username():
    user_data = user_authorization()
    token = user_data["token"]
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().delete(f'/profiles/{user_name}/follow',
                                headers=headers)
    assert response.status_code == 200
    assert response.json()["profile"]["username"] == user_name
    assert response.json()["profile"]["following"] is False
    assert S(profile) == response.json()
