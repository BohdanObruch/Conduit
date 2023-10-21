from allure import step
from demo_apps_project_tests.model.authorization import login_user
from demo_apps_project_tests.helpers import app
from selene import browser, have, be, command, query
from selene.support.shared.jquery_style import s, ss


def test_subscribe_to_user():
    with step('Before'):
        login_user()

    with step('Delete all my articles'):
        app.article_page.deleting_created_posts()

    with step('Checking for a subscription'):
        app.website.go_to_home_page()
        app.article_page.go_to_your_feed_tab()

    with step('Unsubscribe from user by unfollowing him'):
        app.article_page.unfollow_subscriptions()

    with step('Subscribe to user by following him'):
        app.article_page.follow_subscriptions()


def test_personal_article_feed():
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
            app.article_page.check_subscription()
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


def test_unsubscribe_from_user():
    with step('Before'):
        login_user()

    with step('Delete all my articles'):
        app.article_page.deleting_created_posts()

    with step('Checking for a subscription'):
        app.website.go_to_home_page()

        app.article_page.go_to_your_feed_tab()

    with step('Checking the existence of created articles and deleting them if they exist'):
        app.article_page.follow_subscriptions()

    with step('Unsubscribe from user by unfollowing him'):
        app.article_page.unfollow_subscriptions()
