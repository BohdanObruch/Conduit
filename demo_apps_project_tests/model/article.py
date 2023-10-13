import random
import re

from demo_apps_project_tests.data.fake_data import generate_random_article
from demo_apps_project_tests.model.authorization import user_authorization, user_name
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
    browser.element('.article-page h1').with_(timeout=4).should(have.text(title))
    return title


def selection_of_a_random_article():
    num_article = random.randint(0, 9)
    browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=5).should(have.no.visible)
    article_title = (browser.all('article-list article-preview').element(index=num_article).element('h1')
                     .get(query.text_content))
    return article_title


def choosing_a_random_tag():
    num_tag = random.randint(0, 9)
    list_tags = browser.all('.tag-list a').element(index=num_tag)
    tag = list_tags.get(query.text_content)
    list_tags.click()
    return tag


def checking_selected_tag(tag):
    browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=5).should(have.no.visible)
    articles = len(browser.all('article-list article-preview'))

    for i in range(1, articles + 1):
        (browser.all(f'article-list article-preview:nth-child({i}) .tag-list li').element_by(have.text(tag))
         .should(be.visible))


def switch_to_random_page():
    num_page = random.randint(1, 9)
    page_pagination = browser.all('.pagination li').element(index=num_page)
    page_pagination.element('a').perform(command.js.scroll_into_view).click()
    page_pagination.should(have.css_class('active'))


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


def like_unlike_article():
    browser.element('.navbar').perform(command.js.scroll_into_view)
    counter = browser.element('.banner .article-meta favorite-btn .counter')
    button_likes = '.banner .article-meta favorite-btn'

    amount_of_likes = counter.get(query.text_content)
    amount = int(re.sub(r'[()]|\s', '', amount_of_likes))

    text = browser.all(button_likes).first.element('span').get(query.text_content)
    text = text.strip()

    browser.element(button_likes).click()
    browser.element('.article-meta favorite-btn button.disabled').should(be.not_.in_dom)

    likes = counter.get(query.text_content)

    new_amount_of_likes = int(re.sub(r'[()]|\s', '', likes))

    if text == 'Favorite Article':
        assert new_amount_of_likes == amount + 1
    else:
        assert new_amount_of_likes == amount - 1


def deleting_created_posts():
    while browser.element('article-list article-preview').with_(timeout=5).matching(be.visible):
        browser.element('article-list article-preview:nth-child(1) h1').with_(timeout=5).click()
        browser.element('.banner .article-meta [ng-click*="delete"]').click()
        browser.should(have.url_containing('/#/'))
        browser.element('.feed-toggle ul > li:nth-child(2) a').click().should(have.css_class('active'))
        browser.element(f'.navbar [href="#/@{user_name}"]').with_(timeout=5).click()

        browser.should(have.url_containing(f'/#/@{user_name}')).with_(timeout=5)
        browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)


def unfollow_subscriptions():
    while browser.element('article-list article-preview').with_(timeout=5).matching(be.visible):
        browser.element('article-list article-preview:nth-child(1) h1').with_(timeout=5).click()
        browser.element('.banner .article-meta [user$="article.author"] button').perform(
            command.js.scroll_into_view).click()
        browser.element('.banner .article-meta [user$="article.author"] button').with_(timeout=5).should(
            have.text('Follow'))
        author_name = browser.element('.banner .article-meta .author').get(query.text_content)

        browser.element('.navbar [show-authed="true"] a[href="#/"]').click()
        browser.should(have.url_containing('/#/'))
        browser.element('.feed-toggle ul > li:nth-child(1) a').click().should(have.css_class('active')).should(
            have.text('Your Feed'))
        browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)
        browser.all('.article-preview .article-meta a.author').element_by(
            have.text(author_name)).should(be.not_.visible)


def follow_subscriptions():
    if browser.element('article-list article-preview').with_(timeout=5).matching(be.not_.visible):
        browser.element('.feed-toggle ul > li:nth-child(2) a').click().should(have.css_class('active')).should(
            have.text('Global Feed'))
        browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)
        browser.all('article-list article-preview').with_(timeout=5).should(have.size(10))

        browser.element('article-list article-preview:nth-child(1) h1').with_(timeout=5).click()
        browser.element('.banner .article-meta [user$="article.author"] button').perform(
            command.js.scroll_into_view).should(have.text('Follow')).click()
        author_name = browser.element('.banner .article-meta .author').get(query.text_content)
        browser.element('.banner .article-meta [user$="article.author"] button').with_(timeout=5).should(
            have.text('Unfollow'))

        browser.element('.navbar [show-authed="true"] a[href="#/"]').click()
        browser.should(have.url_containing('/#/'))

        browser.element('.feed-toggle ul > li:nth-child(1) a').should(have.css_class('active')).should(
            have.text('Your Feed'))
        browser.element('article-list article-preview').with_(timeout=5).should(be.visible)

        browser.all('.article-preview .article-meta a.author').element_by(have.text(author_name)).should(be.visible)


