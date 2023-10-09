from selene import browser, have
from demo_apps_project_tests.model.article import check_articles


def test_display_article_list(browser_management):
    browser.open('/')

    browser.should(have.url_containing('/#/'))

    browser.all('article-list article-preview').should(have.size(10))

    check_articles()

