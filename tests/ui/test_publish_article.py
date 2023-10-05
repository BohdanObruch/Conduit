from selene import browser, be, have
from demo_apps_project_tests.model.authorization import login_user
from demo_apps_project_tests.data.fake_data import title_article, description_article, body_article
from demo_apps_project_tests.utils.requests_helper import input_tags, checking_tags


def test_publish_article(browser_management):
    login_user()

    browser.should(have.url_containing('/#/'))

    browser.element('[href="#/editor/"]').click()
    browser.should(have.url_containing('/#/editor/'))

    browser.element('.editor-page').should(be.visible)

    browser.element('[ng-model$=title]').type(title_article)
    browser.element('[ng-model$=description]').type(description_article)
    browser.element('[ng-model$=body]').type(body_article)
    input_tags()
    browser.element('[type=button]').click()

    browser.should(have.url_containing(f'/#/article/{title_article}'))
    browser.element('.banner h1').should(have.text(title_article))
    browser.element('[ng-bind-html$=body]').should(have.text(body_article))
    checking_tags()
