from demo_apps_project_tests.data.fake_data import generate_random_article
from demo_apps_project_tests.model.authorization import user_authorization
from demo_apps_project_tests.utils.sessions import conduit
from tests.conftest import dotenv


slug = dotenv.get('SLUG')


def create_article():
    article_data = generate_random_article()
    user_data = user_authorization()
    token = user_data["token"]
    title_article = article_data["title"]
    description_article = article_data["description"]
    body_article = article_data["body"]
    tags_article = article_data["tags"]
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
    slug_article = response.json()["article"]["slug"]
    return slug_article, token


def create_a_comment_for_article():
    article_data = generate_random_article()
    token = user_authorization()["token"]
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
    id_comment = response.json()["comment"]["id"]
    return id_comment, token