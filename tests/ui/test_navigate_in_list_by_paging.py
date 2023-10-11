from selene import browser, have, command
from demo_apps_project_tests.model.article import selection_of_a_random_article, switch_to_random_page


def test_navigate_in_list_by_pagination(browser_management):
    browser.open('/')

    browser.should(have.url_containing('/#/'))

    browser.all('article-list article-preview').should(have.size(10))
    browser.all('.pagination .page-link').should(have.size_greater_than(10))
    browser.all('.pagination').first.element('li').should(have.css_class('active'))

    article_title = selection_of_a_random_article()

    switch_to_random_page()

    browser.all('article-list article-preview').element_by_its('h1', have.no.text(article_title))

    browser.all('.pagination li').first.element('a').perform(command.js.scroll_into_view).click()
    browser.all('.pagination').first.element('li').should(have.css_class('active'))
    browser.all('article-list article-preview').element_by_its('h1', have.text(article_title))



