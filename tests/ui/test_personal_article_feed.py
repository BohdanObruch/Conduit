from selene import browser, have, be, command, query
from demo_apps_project_tests.model.article import open_random_article
from demo_apps_project_tests.model.authorization import login_user


def test_personal_article_feed(browser_management):
    login_user()

    browser.element('.feed-toggle ul > li:nth-child(2) a').click().should(have.css_class('active')).should(
        have.text('Global Feed'))

    article = open_random_article()
    url_title = article.replace(" ", "-").replace(",", "")
    browser.should(have.url_containing(f'/#/article/{url_title}'))

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
