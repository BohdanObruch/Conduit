import random

from demo_apps_project_tests.data.fake_data import generate_random_article
from demo_apps_project_tests.model.authorization import user_authorization
from demo_apps_project_tests.utils.sessions import conduit
from selene import browser, have, be, query, command
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


def clear_article():
    browser.element('[ng-model$=title]').clear()
    browser.element('[ng-model$=description]').clear()
    browser.element('[ng-model$=body]').clear()
    delete_tags()


def fill_article():
    article = generate_random_article()
    browser.element('[ng-model$=title]').type(article["title"])
    browser.element('[ng-model$=description]').type(article["description"])
    browser.element('[ng-model$=body]').type(article["body"])
    input_tags(article)
    browser.element('[type=button]').with_(timeout=5).click()
    return article


def checking_tags(article):
    for tag in article["tags"]:
        browser.element('.tag-list').should(have.text(tag))


def input_tags(article):
    for tag in article["tags"]:
        browser.element('[ng-model$=tagField]').type(tag).press_enter()


def delete_tags():
    article_tags = len(browser.all('.tag-list span'))
    for tag in range(article_tags):
        browser.element('[ng-click*=remove]').click()


def open_random_article():
    num_article = random.randint(0, 9)
    browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=5).should(have.no.visible)
    browser.all('article-list article-preview').should(have.size(10))
    article_title = browser.all('article-list article-preview').element(index=num_article).element('h1')
    article_title.perform(command.js.scroll_into_view).click()

    title = article_title.get(query.text_content)

    browser.should(have.url_containing(f'/#/article/'))
    browser.element('.article-page h1').should(have.text(title))


def check_articles():
    for i in range(1, 11):
        browser.element(f'article-preview:nth-child({i}) .date').should(be.visible)
        browser.element(f'article-preview:nth-child({i}) .author').should(be.visible)
        browser.element(f'article-preview:nth-child({i}) .info').should(be.visible)
        browser.element(f'article-preview:nth-child({i}) img').get(query.attribute('src'))
        browser.element(f'article-preview:nth-child({i}) favorite-btn span').should(be.visible)
        browser.element(f'article-preview:nth-child({i}) h1').should(be.visible)
        browser.element(f'article-preview:nth-child({i}) p').should(be.visible)
        browser.element(f'article-preview:nth-child({i}) .tag-list').should(be.visible)
