from selene import have, command
from allure import step
from selene.support.shared.jquery_style import ss
from demo_apps_project_tests.helpers import app


def test_navigate_in_list_by_pagination(browser_management):
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
