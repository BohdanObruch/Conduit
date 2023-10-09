from selene import browser, have
from demo_apps_project_tests.model.article import open_random_article, like_unlike_article
from demo_apps_project_tests.model.authorization import login_user


def test_like_article(browser_management):
    login_user()

    browser.element('.feed-toggle ul > li:nth-child(2) a').click().should(have.css_class('active'))

    browser.all('article-list article-preview').with_(timeout=5).should(have.size(10))

    open_random_article()

    like_unlike_article()
