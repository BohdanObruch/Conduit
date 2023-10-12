from selene import browser, have, be
from demo_apps_project_tests.model.article import deleting_created_posts, follow_subscriptions, unfollow_subscriptions
from demo_apps_project_tests.model.authorization import login_user, user_name


def test_unsubscribe_from_user(browser_management):
    login_user()

    browser.element(f'.navbar [href="#/@{user_name}"]').with_(timeout=5).click()
    browser.should(have.url_containing(f'/#/@{user_name}'))

    browser.element('.articles-toggle > ul > li:first-child a').should(be.present).should(have.text('My Articles'))

    browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)

    deleting_created_posts()

    browser.element('.navbar [show-authed="true"] a[href="#/"]').click()
    browser.should(have.url_containing('/#/'))

    browser.element('.feed-toggle ul > li:nth-child(1) a').click().should(have.css_class('active')).should(
        have.text('Your Feed'))
    browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)

    follow_subscriptions()

    browser.element('.feed-toggle ul > li:nth-child(1) a').should(have.css_class('active')).should(
        have.text('Your Feed'))
    browser.element('article-list article-preview').with_(timeout=5).should(be.visible)
    browser.element('.article-preview .article-meta a.author').should(be.visible)

    unfollow_subscriptions()
