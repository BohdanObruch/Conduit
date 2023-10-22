from selene.support.shared.jquery_style import ss
from allure import step
from selene import have
from demo_apps_project_tests.model.authorization import login_user
from demo_apps_project_tests.helpers import app


def test_add_comment(setup_browser):
    with step('Before'):
        login_user()

    with step('Open random article'):
        with step('Go to global feed tab'):
            app.article_page.go_to_global_feed_tab()
        with step('Open random article'):
            app.article_page.open_random_article()

    with step('Add comment'):
        app.article_page.add_comment()


def test_delete_comment(setup_browser):
    with step('Before'):
        login_user()

    with step('Open random article'):
        with step('Go to global feed tab'):
            app.article_page.go_to_global_feed_tab()
        with step('Open random article'):
            app.article_page.open_random_article()

    with step('Add comment'):
        article = app.article_page.add_comment()

    with step('Delete comment'):
        with step('Search comment'):
            delete_comment = ss('.article-page comment').with_(timeout=5).element_by_its(
                                                                    'p', have.exact_text(article["comments"]))
        with step('Click delete comment button'):
            delete_comment.element('.card-footer [ng-click*="delete"]').click()
        with step('Check that the comment that has been deleted is not displayed'):
            delete_comment.should(have.no.visible)
