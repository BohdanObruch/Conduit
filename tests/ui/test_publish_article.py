from selene import browser, be, have
from demo_apps_project_tests.model.authorization import login_user
from demo_apps_project_tests.model.article import checking_tags, fill_article


def test_publish_article(browser_management):
    login_user()

    browser.should(have.url_containing('/#/'))

    browser.element('[href="#/editor/"]').click()
    browser.should(have.url_containing('/#/editor/'))

    browser.element('.editor-page').should(be.visible)

    article = fill_article()
    url_title = article["title"].replace(" ", "-")
    browser.should(have.url_containing(f'/#/article/{url_title}'))
    browser.element('.banner h1').should(have.text(article["title"]))
    browser.element('[ng-bind-html$=body]').should(have.text(article["body"]))
    checking_tags(article)
