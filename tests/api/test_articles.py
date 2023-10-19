from demo_apps_project_tests.data.fake_data import generate_random_article
from demo_apps_project_tests.model.article import create_article, slug
from demo_apps_project_tests.model.authorization import user_authorization
from schemas.conduit import *
from pytest_voluptuous import S
from demo_apps_project_tests.utils.sessions import conduit
from allure import tag, title
from tests.conftest import dotenv


tag_name = dotenv.get('TAG_NAME')
author = dotenv.get('AUTHOR')


@tag('API')
@title("Get most recent articles from users you follow")
def test_getting_new_articles_from_users_follow():
    user_data = user_authorization()
    token = user_data["token"]
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().get(f'/articles/feed',
                             headers=headers
                             )
    assert response.status_code == 200
    assert response.json()['articles'][0]['author']['following'] is True
    assert S(articles_follow_and_global) == response.json()


@tag('API')
@title("Get most recent articles globally")
def test_most_recent_articles():
    params = {
        "tag": tag_name,
        "author": author,
        "offset": 1,
        "limit": 20

    }
    response = conduit().get(f'/articles/',
                             params=params
                             )
    assert response.status_code == 200
    assert response.json()['articles'][0]['author']['username'] == author
    assert tag_name in response.json()['articles'][0]['tagList']
    assert S(articles_follow_and_global) == response.json()


@tag('API')
@title("Create an article")
def test_create_an_article():
    article_data = generate_random_article()
    user_data = user_authorization()
    title_article = article_data["title"]
    description_article = article_data["description"]
    body_article = article_data["body"]
    tags_article = article_data["tags"]
    token = user_data["token"]
    data = {
        "article": {
            "title": title_article,
            "description": description_article,
            "body": body_article,
            "tagList": tags_article,
        }
    }

    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().post(f'/articles',
                              headers=headers,
                              json=data
                              )
    assert response.status_code == 201
    assert response.json()["article"]["title"] == title_article
    assert response.json()["article"]["description"] == description_article
    assert response.json()["article"]["body"] == body_article
    assert S(article) == response.json()


@tag('API')
@title("Get an article")
def test_get_an_article():
    response = conduit().get(f'/articles/{slug}'
                             )
    assert response.status_code == 200
    assert response.json()["article"]["slug"] == slug
    assert S(article) == response.json()


@tag('API')
@title("Update an article")
def test_update_an_article():
    article_data = create_article()
    slug_article = article_data[0]
    token = article_data[1]
    random_article_data = generate_random_article()
    article_title = random_article_data["title"]
    description = random_article_data["description"]
    body = random_article_data["body"]

    data = {
        "article": {
            "title": article_title,
            "description": description,
            "body": body
        }
    }

    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().put(f'/articles/{slug_article}',
                             headers=headers,
                             json=data
                             )
    assert response.status_code == 200
    assert response.json()["article"]["title"] == article_title
    assert response.json()["article"]["description"] == description
    assert response.json()["article"]["body"] == body
    assert S(article) == response.json()


@tag('API')
@title("Delete an article")
def test_delete_an_article():
    slug_article = create_article()[0]
    token = create_article()[1]
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().delete(f'/articles/{slug_article}',
                                headers=headers
                                )
    assert response.status_code == 204
    assert response.text == ""
