from demo_apps_project_tests.data.fake_data import *
from demo_apps_project_tests.model.article import create_a_comment_for_article
from demo_apps_project_tests.model.authorization import user_authorization
from schemas.conduit import *
from pytest_voluptuous import S
from demo_apps_project_tests.utils.sessions import conduit
from allure import tag, title
from tests.conftest import dotenv


slug = dotenv.get('SLUG')


@tag('API')
@title("Get the comments for an article")
def test_get_the_comments_for_an_article():
    user_data = user_authorization()
    token = user_data["token"]
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
def test_create_a_comment_for_an_article():
    user_data = user_authorization()
    token = user_data["token"]
    article_data = generate_random_article_data()
    body_article = article_data["body"]
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
def test_delete_a_comment():
    comment_data = create_a_comment_for_article()
    id_comment = comment_data[0]
    token = comment_data[1]
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().delete(f'/articles/{slug}/comments/{id_comment}',
                                headers=headers
                                )
    assert response.status_code == 200
    assert response.json() == {}
