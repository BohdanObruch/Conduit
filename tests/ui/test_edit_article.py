from selene import browser, be, have

from demo_apps_project_tests.model.article import clear_article, fill_article, checking_tags
from demo_apps_project_tests.model.authorization import login_user
from tests.conftest import dotenv

user_name = dotenv.get('USERNAME')


def test_edit_article(browser_management):
    login_user()

    browser.should(have.url_containing('/#/'))

    browser.element('[href="#/editor/"]').click()
    browser.should(have.url_containing('/#/editor/'))

    browser.element('.editor-page').should(be.visible)

    title_article = fill_article()
    url_title = title_article["title"].replace(" ", "-")
    browser.should(have.url_containing(f'/#/article/{url_title}'))

    browser.element(f'.navbar [href="#/@{user_name}"]').with_(timeout=5).click()
    browser.should(have.url_containing(f'/#/@{user_name}'))

    browser.element('.articles-toggle > ul > li:first-child a').should(be.present)

    browser.all('article-preview').element_by_its('.preview-link', be.visible).element('h1').click()

    browser.element('.article-actions a[href*="#/editor"]').click()
    browser.should(have.url_containing('/#/editor/')).with_(timeout=5)

    browser.element('.editor-page').should(be.visible)

    clear_article()

    article = fill_article()
    new_url_title = article["title"].replace(" ", "-")
    browser.should(have.url_containing(f'/#/article/{new_url_title}'))
    browser.element('.banner h1').should(have.text(article["title"]))
    browser.element('[ng-bind-html$=body]').should(have.text(article["body"]))
    checking_tags(article)

