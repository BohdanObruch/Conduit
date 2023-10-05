from demo_apps_project_tests.model.authorization import user_authorization
from schemas.conduit import *
from pytest_voluptuous import S
from demo_apps_project_tests.utils.sessions import conduit
from allure import tag, title
from tests.conftest import dotenv

slug = dotenv.get('SLUG')


@tag('API')
@title("Add article to favorites")
def test_add_article_to_favorites():
    user_data = user_authorization()
    token = user_data["token"]
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().post(f'/articles/{slug}/favorite',
                              headers=headers
                              )
    assert response.status_code == 200
    assert response.json()["article"]["slug"] == slug
    assert S(articles) == response.json()


@tag('API')
@title("Remove article from favorites")
def test_remove_article_from_favorites():
    user_data = user_authorization()
    token = user_data["token"]
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().delete(f'/articles/{slug}/favorite',
                                headers=headers
                                )
    assert response.status_code == 200
    assert response.json()["article"]["slug"] == slug
    assert S(articles) == response.json()
