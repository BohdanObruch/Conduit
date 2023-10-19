from selene import have
from allure import step
from selene.support.shared.jquery_style import s, ss
from demo_apps_project_tests.helpers import app


def test_filter_articles_by_tag(setup_browser):
    with step('Before'):
        app.website.open_website()

    with step('Select random tag'):
        with step('Checking the display of the tag list must be greater than 5'):
            ss('.tag-list a').with_(timeout=10).should(have.size_greater_than(5))
        with step('Select random tag'):
            tag = app.article_page.choosing_a_random_tag()

    with step('Check articles list'):
        with step('Checking the display active tab with selected tag'):
            feed = s('.feed-toggle')
            feed.all('.nav-item').element_by_its('a', have.css_class('active')).should(have.text(tag))
        with step('Checking the display all articles with selected tag'):
            app.article_page.checking_selected_tag(tag)
