from selene import browser, be, have
from demo_apps_project_tests.model.authorization import login_user
from allure import step
from selene.support.shared.jquery_style import s
from demo_apps_project_tests.helpers import app


def test_edit_article(setup_browser):
    with step('Before'):
        login_user()

    with step('Add article'):
        app.article_page.open_add_new_article_page()
        with step('Fill form'):
            title_article = app.article_page.fill_article()
        with step('Checking created article'):
            url_title = title_article["title"].replace(" ", "-")
            browser.should(have.url_containing(f'/#/article/{url_title}'))

    with step('Find article'):
        with step('Go to user page'):
            app.website.going_to_user_page()
        with step('Checking page activity'):
            s('.articles-toggle > ul > li:first-child a').with_(timeout=6).should(have.css_class('active'))
        with step('Open article'):
            app.article_page.select_first_article()
        with step('Click edit article button'):
            s('.article-actions a[href*="#/editor"]').click()

    with step('Edit article'):
        with step('Checking url'):
            browser.should(have.url_containing('/#/editor/')).with_(timeout=5)
        with step('Checking the display of the form'):
            s('.editor-page form').should(be.visible)
        with step('Clear form'):
            app.article_page.clear_article()
        with step('Fill form new data'):
            article = app.article_page.fill_article()

    with step('Check article data'):
        app.article_page.check_article_data(article)
