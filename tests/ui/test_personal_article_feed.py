from selene import browser, have, be, command, query
from demo_apps_project_tests.model.authorization import login_user
from selene.support.shared.jquery_style import s, ss
from allure import step
from demo_apps_project_tests.helpers import app


def test_personal_article_feed(setup_browser):
    with step('Before'):
        login_user()

    with step('Open random article'):
        with step('Go to Global Feed tab'):
            app.article_page.go_to_global_feed_tab()
        with step('Selection of random article'):
            article = app.article_page.open_random_article()
        with step('Checking url article'):
            url_title = article.replace(" ", "-").replace(",", "")
            browser.should(have.url_containing(f'/#/article/{url_title}'))

    with step('Follow author'):
        with step('Click Follow on author'):
            s('.banner .article-meta [user$="article.author"] button').perform(
                command.js.scroll_into_view).should(have.text('Follow')).click()
        with step('Get author name'):
            author_name = s('.banner .article-meta .author').get(query.text_content)
        with step('Checking Follow on author'):
            s('.banner .article-meta [user$="article.author"] button').with_(timeout=5).should(
                have.text('Unfollow'))
    with step('Check user in your subscription list'):
        with step('Go to Home page'):
            app.website.go_to_home_page()
        with step('Go to Your Feed tab'):
            app.article_page.go_to_your_feed_tab()
        with step('Check user in your subscription list'):
            ss('.article-preview .article-meta a.author').element_by(have.text(author_name)).should(be.visible)
