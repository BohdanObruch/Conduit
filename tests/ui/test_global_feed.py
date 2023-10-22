from demo_apps_project_tests.helpers import app
from allure import step
from demo_apps_project_tests.model.authorization import login_user
from selene import have, command
from selene.support.shared.jquery_style import s, ss


def test_display_article_list(setup_browser):
    with step('Before'):
        app.website.open_website()

    with step('Check article list'):
        app.article_page.check_article_list()

    with step('Check article card'):
        app.article_page.check_articles()


def test_open_article_detail_page(setup_browser):
    with step('Before'):
        app.website.open_website()

    with step('Open random article'):
        app.article_page.open_random_article()


def test_like_article(setup_browser):
    with step('Before'):
        login_user()

        with step('Open global feed tab'):
            app.article_page.go_to_global_feed_tab()

    with step('Select random article'):
        article_title = app.article_page.selection_of_a_random_article()

    with step('Like/unlike article'):
        app.article_page.like_unlike_article(article_title)


def test_navigate_in_list_by_pagination(setup_browser):
    with step('Before'):
        app.website.open_website()

        with step('Check for more than 10 pagination pages'):
            ss('.pagination .page-link').should(have.size_greater_than(10))
        with step('Checking the activity of the first page'):
            ss('.pagination').first.element('li').should(have.css_class('active'))

    with step('Select random article'):
        article_title = app.article_page.selection_of_a_random_article()

    with step('Navigate to random page'):
        app.article_page.switch_to_random_page()
        with step('Checking not showing article from page'):
            ss('article-list article-preview').element_by_its('h1', have.no.text(article_title))

    with step('Navigate back to 1st page'):
        with step('Going to first page'):
            ss('.pagination li').first.element('a').perform(command.js.scroll_into_view).click()
        with step('Checking the activity of the first page'):
            ss('.pagination').first.element('li').should(have.css_class('active'))
        with step('Checking showing article from page'):
            ss('article-list article-preview').element_by_its('h1', have.text(article_title))


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
