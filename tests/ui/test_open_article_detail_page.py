from selene import browser, have
from demo_apps_project_tests.model.article import open_random_article


def test_open_article_detail_page(browser_management):
    browser.open('/')

    browser.should(have.url_containing('/#/'))

    browser.all('article-list article-preview').should(have.size(10))

    open_random_article()
