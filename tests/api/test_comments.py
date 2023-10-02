from demo_apps_project_tests.data.fake_data import *
from schemas.conduit import *
from pytest_voluptuous import S
from demo_apps_project_tests.utils.sessions import conduit
from allure import tag, title
from tests.conftest import dotenv


slug = dotenv.get('SLUG')


@tag('API')
@title("Get the comments for an article")
def test_get_the_comments_for_an_article(user_authorization):
    token = user_authorization[0]
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().get(f'/articles/{slug}/comments',
                             headers=headers
                             )
    assert response.status_code == 200
    assert S(comments) == response.json()


@tag('API')
@title("Create a comment for an article")
def test_create_a_comment_for_an_article(user_authorization):
    token = user_authorization[0]
    data = {
        "comment": {
            "body": body_article}
            }
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().post(f'/articles/{slug}/comments',
                              headers=headers,
                              json=data
                              )
    assert response.status_code == 200
    assert response.json()["comment"]["body"] == body_article
    assert S(add_comment) == response.json()


@tag('API')
@title("Delete a comment for an article")
def test_delete_a_comment(create_a_comment_for_article):
    id_comment = create_a_comment_for_article[0]
    token = create_a_comment_for_article[1]
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().delete(f'/articles/{slug}/comments/{id_comment}',
                                headers=headers
                                )
    assert response.status_code == 200
    assert response.json() == {}
