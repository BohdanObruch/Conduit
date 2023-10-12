from selene import browser, have
from demo_apps_project_tests.model.article import choosing_a_random_tag, checking_selected_tag


def test_filter_articles_by_tag(browser_management):
    browser.open('/')

    browser.should(have.url_containing('/#/'))

    browser.all('article-list article-preview').should(have.size(10))
    browser.all('.tag-list a').with_(timeout=10).should(have.size_greater_than(5))

    tag = choosing_a_random_tag()

    feed = browser.element('.feed-toggle')
    feed.all('.nav-item').element_by_its('a', have.css_class('active')).should(have.text(tag))

    checking_selected_tag(tag)

