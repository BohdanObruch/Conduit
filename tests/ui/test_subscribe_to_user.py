from selene import browser, have, be
from demo_apps_project_tests.model.article import checking_created_posts, checking_subscriptions
from demo_apps_project_tests.model.authorization import login_user, user_name


def test_subscribe_to_user(browser_management):
    login_user()

    browser.element(f'.navbar [href="#/@{user_name}"]').with_(timeout=5).click()
    browser.should(have.url_containing(f'/#/@{user_name}'))

    browser.element('.articles-toggle > ul > li:first-child a').should(be.present).should(have.text('My Articles'))

    browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)

    checking_created_posts()

    browser.element('.navbar [show-authed="true"] a[href="#/"]').click()
    browser.should(have.url_containing('/#/'))

    browser.element('.feed-toggle ul > li:nth-child(1) a').click().should(have.css_class('active')).should(
        have.text('Your Feed'))
    browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)

    checking_subscriptions()

    browser.element('.feed-toggle ul > li:nth-child(2) a').click().should(have.css_class('active')).should(
        have.text('Global Feed'))
    browser.element('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)
    browser.all('article-list article-preview').should(have.size(10))

    browser.element('article-list article-preview:nth-child(1) h1').click()

    browser.element('.banner .article-meta [user$="article.author"] button').with_(timeout=5).should(
        have.text('Follow')).click()
    browser.element('.banner .article-meta [user$="article.author"] button').with_(timeout=5).should(
        have.text('Unfollow'))

    browser.element('.navbar [show-authed="true"] a[href="#/"]').click()
    browser.should(have.url_containing('/#/'))
    browser.element('.feed-toggle ul > li:nth-child(1) a').click().should(have.css_class('active')).should(
        have.text('Your Feed'))

    browser.element('article-list article-preview').with_(timeout=5).should(be.visible)
    browser.element('.article-preview .article-meta a.author').should(be.visible)
