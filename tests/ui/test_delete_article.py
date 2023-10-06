from selene import browser, be, have
from demo_apps_project_tests.model.authorization import login_user
from demo_apps_project_tests.model.article import fill_article
from tests.conftest import dotenv

user_name = dotenv.get('USERNAME')


def test_delete_article(browser_management):
    login_user()

    browser.should(have.url_containing('/#/'))

    browser.element('[href="#/editor/"]').click()
    browser.should(have.url_containing('/#/editor/'))

    browser.element('.editor-page').should(be.visible)

    article = fill_article()

    url_title = article["title"].replace(" ", "-")
    browser.should(have.url_containing(f'/#/article/{url_title}'))

    browser.element(f'.navbar [href="#/@{user_name}"]').with_(timeout=5).click()
    browser.should(have.url_containing(f'/#/@{user_name}'))

    browser.element('.articles-toggle > ul > li:first-child a').should(be.present)

    browser.all('article-preview').element_by_its('.preview-link', be.visible).element('h1').click()

    browser.element('.article-actions span:not(.ng-hide) button').click()
    browser.should(have.url_containing('/#/')).with_(timeout=5)
    browser.element('article-list article-preview').should(be.visible)

    browser.element(f'.navbar [href="#/@{user_name}"]').with_(timeout=5).click()
    browser.should(have.url_containing(f'/#/@{user_name}'))

    browser.all('article-list').element('article-preview h1').should(have.no.text(article["title"]))





