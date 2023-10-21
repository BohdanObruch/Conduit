import random
from demo_apps_project_tests.data.fake_data import generate_random_article
from demo_apps_project_tests.helpers import app
from selene.support.shared.jquery_style import s, ss
from selene import browser, have, be, command, query
from allure import step


class ArticlePage:
    def clear_article(self):
        s('[ng-model$=title]').clear()
        s('[ng-model$=description]').clear()
        s('[ng-model$=body]').clear()
        self.delete_tags()
        return self

    def fill_article(self):
        with step('Generate article data'):
            article = generate_random_article()
        with step('Fill form'):
            with step('Fill title'):
                s('[ng-model$=title]').type(article["title"])
            with step('Fill description'):
                s('[ng-model$=description]').type(article["description"])
            with step('Fill body'):
                s('[ng-model$=body]').type(article["body"])
            with step('Fill tags'):
                self.input_tags(article)
        with step('Save article'):
            with step('Click on the Publish Article button'):
                s('[type=button]').with_(timeout=5).click()
        return article

    def checking_tags(self, article):
        with step('Checking tags in article'):
            for tag in article["tags"]:
                s('.tag-list').should(have.text(tag))
        return self

    def input_tags(self, article):
        with step('Add tags'):
            for tag in article["tags"]:
                s('[ng-model$=tagField]').type(tag).press_enter()
        return self

    def delete_tags(self):
        article_tags = len(ss('.tag-list span'))
        for tag in range(article_tags):
            s('[ng-click*=remove]').click()
        return self

    @staticmethod
    def open_random_article():
        with step('Selection of random articles from 1 to 10 per page'):
            num_article = random.randint(0, 9)
        with step('Checking no showing loader on page'):
            s('article-list .article-preview[ng-hide$="loading"]').with_(timeout=5).should(have.no.visible)
        with step('Checking the availability of 10 articles on the page'):
            ss('article-list .article-preview').wait_until(have.size(10))
        with step('Click on the title of the article'):
            article_title = ss('article-list article-preview').element(index=num_article).element('h1')
            article_title.perform(command.js.scroll_into_view).click()
        with step('Get article title'):
            title = article_title.get(query.text_content)
        with step('Check article'):
            with step('Checking the url of an open article'):
                browser.should(have.url_containing(f'/#/article/'))
            with step('Checking the title of the article'):
                s('.article-page h1').perform(command.js.scroll_into_view).with_(timeout=4).should(have.text(title))
            return title

    @staticmethod
    def selection_of_a_random_article():
        with step('Checking 10 articles on the tab'):
            ss('article-list article-preview').should(have.size(10))

        with step('Selection of random articles from 1 to 10 per page'):
            num_article = random.randint(0, 9)
            s('article-list .article-preview[ng-hide$="loading"]').with_(timeout=5).should(have.no.visible)
        with step('Get article title'):
            article_title = (ss('article-list article-preview').element(index=num_article).element('h1')
                             .get(query.text_content))
        return article_title

    @staticmethod
    def choosing_a_random_tag():
        with step('Selection of random tag nuber from 1 to 10'):
            num_tag = random.randint(0, 9)
        with step('List of tags'):
            list_tags = ss('.tag-list a').element(index=num_tag)
        with step('Get tag name'):
            tag = list_tags.get(query.text_content)
        with step('Click on the tag'):
            list_tags.click()
        return tag

    def checking_selected_tag(self, tag):
        with step('Checking no showing loader on page'):
            s('article-list .article-preview[ng-hide$="loading"]').with_(timeout=5).should(have.no.visible)
            ss('article-list article-preview').first.element('.tag-list li').wait_until(have.text(tag))

        with step('Calculate the number of articles with the selected tag'):
            articles = len(ss('article-list article-preview'))

        with step('Checking the availability of articles with the selected tag'):
            for i in range(1, articles + 1):
                (ss(f'article-list article-preview:nth-child({i}) .tag-list li').element_by(have.text(tag))
                 .should(be.visible))
        return self

    def switch_to_random_page(self):
        with step('Switch to random page'):
            with step('Choice random page number from 1 to 10'):
                num_page = random.randint(1, 10)

            with step('Click on the page number'):
                page_pagination = ss('.pagination li').element(index=num_page)
                page_pagination.element('a').perform(command.js.scroll_into_view).click()

            with step('Checking the activity of the selected page'):
                page_pagination.should(have.css_class('active'))
        return self

    def check_articles(self):
        with step('Checking the display of each card of the article: created date, author, '
                  'username, avatar, likes count, title, description, tags'):
            for i in range(1, 11):
                s(f'article-preview:nth-child({i}) .date').should(be.visible)
                s(f'article-preview:nth-child({i}) .author').should(be.visible)
                s(f'article-preview:nth-child({i}) .info').should(be.visible)
                s(f'article-preview:nth-child({i}) img').get(query.attribute('src'))
                s(f'article-preview:nth-child({i}) favorite-btn span').should(be.visible)
                s(f'article-preview:nth-child({i}) h1').should(be.visible)
                s(f'article-preview:nth-child({i}) p').should(be.visible)
                s(f'article-preview:nth-child({i}) .tag-list').should(be.visible)
        return self

    def like_unlike_article(self, article_title):
        with step('Saving the number of likes'):
            random_article = ss('article-list article-preview').element_by_its('h1', have.exact_text(article_title))
            random_article.perform(command.js.scroll_into_view)
            button = random_article.element('favorite-btn span')

            amount = int(button.get(query.text_content))

        with step('Click on the button'):
            random_article.element('favorite-btn').click()
            s('.article-meta favorite-btn button.disabled').should(be.not_.in_dom)

        with step('Saving the new number of likes'):
            new_amount_of_likes = int(button.get(query.text_content))

        with step('Checking the number of likes'):
            status_like = random_article.element('button.btn-primary')
            if status_like.matching(be.present) is True:
                assert new_amount_of_likes == amount + 1
            else:
                assert new_amount_of_likes == amount - 1
        return self

    def deleting_created_posts(self):
        app.website.going_to_user_page()

        with step('Checking the display My Articles page'):
            s('.articles-toggle > ul > li:first-child a').should(be.present).should(
                have.text('My Articles'))
        with step('Checking no showing loader on page'):
            s('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(
                have.no.visible)
        with step('Checking the availability of created articles'):
            while s('article-list article-preview').with_(timeout=5).matching(be.visible):
                self.select_first_article()

                with step('Click on the delete button'):
                    s('.banner .article-meta [ng-click*="delete"]').click()
                with step('Checking the url display after deleting the article'):
                    browser.should(have.url_containing('/#/'))

                self.go_to_global_feed_tab()

                app.website.going_to_user_page()

                with step('Checking the removal of all articles and not displaying on the page'):
                    s('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)
        return self

    def unfollow_subscriptions(self):
        with step('Checking the display of the "Your Feed" page'):
            while s('article-list article-preview').with_(timeout=5).matching(be.visible):
                self.select_first_article()

                with step('Click on the button "Unfollow"'):
                    s('.banner .article-meta [user$="article.author"] button').perform(
                        command.js.scroll_into_view).click()

                with step('Checking the button text "Follow"'):
                    s('.banner .article-meta [user$="article.author"] button').with_(timeout=5).should(
                        have.text('Follow'))

                with step('Get and remember the author name'):
                    author_name = s('.banner .article-meta .author').get(query.text_content)

                app.website.go_to_home_page()

                self.go_to_your_feed_tab()

                with step('Checking the absence of the name of the unsubscribed author'):
                    ss('.article-preview .article-meta a.author').element_by(have.text(author_name)).should(
                        be.not_.visible)
        return self

    def follow_subscriptions(self):
        if s('article-list article-preview').with_(timeout=7).matching(be.not_.visible):
            with step('Select first article'):
                self.go_to_global_feed_tab()
                self.select_first_article()

            with step('Click on the button "Follow"'):
                s('.banner .article-meta [user$="article.author"] button').perform(
                    command.js.scroll_into_view).should(have.text('Follow')).click()

            with step('Get and remember the author name'):
                author_name = s('.banner .article-meta .author').get(query.text_content)
            with step('Checking the button text "Unfollow"'):
                s('.banner .article-meta [user$="article.author"] button').with_(timeout=5).should(
                    have.text('Unfollow'))

            with step('Check user in your subscription list'):
                app.website.go_to_home_page()

                self.go_to_your_feed_tab()

                with step("Check the author's name must be visible on the page"):
                    ss('.article-preview .article-meta a.author').element_by(have.text(author_name)).should(be.visible)
        return self

    def go_to_your_feed_tab(self):
        with step('Checking the display of the "Your Feed" page'):
            s('.feed-toggle ul > li:nth-child(1) a').should(have.css_class('active')).should(
                have.text('Your Feed'))
        with step('Checking no showing loader on page'):
            s('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)
        return self

    def go_to_global_feed_tab(self):
        with step('Click on the "Global Feed" tab'):
            s('.feed-toggle ul > li:nth-child(2) a').click().should(have.css_class('active')).should(
                have.text('Global Feed'))
        with step('Checking no showing loader on page'):
            s('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)
        with step('Checking 10 articles on the tab'):
            ss('article-list article-preview').should(have.size(10))
        return self

    def select_first_article(self):
        with step('Select and click first article title'):
            s('article-list article-preview:nth-child(1) h1').with_(timeout=5).click()
        with step('Checking the url display the article'):
            browser.with_(timeout=5).should(have.url_containing('/#/article/'))
        return self

    def check_article_list(self):
        with step('Checking the display of the "Global Feed" page'):
            s('.feed-toggle ul > li:nth-child(2) a').should(have.css_class('active')).should(
                have.text('Global Feed'))
        with step('Checking no showing loader on page'):
            s('article-list .article-preview[ng-hide$="loading"]').with_(timeout=7).should(have.no.visible)
        with step('Checking 10 articles on the tab'):
            ss('article-list article-preview').should(have.size(10))
        return self

    @staticmethod
    def add_comment():
        with step('Generate random article data'):
            article = generate_random_article()
        with step('Scrolling and add comment to article'):
            s('textarea[ng-model$=body]').perform(command.js.scroll_into_view).click().type(article["comments"])
        with step('Click on post comment'):
            s('button[type=submit]').click()
        with step('Check that comment was added'):
            s('comment .card').perform(command.js.scroll_into_view)
            ss('.article-page comment').with_(timeout=5).element_by_its('p', have.text(article["comments"]))
        return article

    def open_add_new_article_page(self):
        with step('Click on New Article'):
            s('[href="#/editor/"]').click()
        with step('Checking url'):
            browser.should(have.url_containing('/#/editor/'))
        with step('Checking the display of the form'):
            s('.editor-page form').should(be.visible)
        return self

    def check_article_data(self, article):
        with step('Checking the url'):
            url_title = article["title"].replace(" ", "-")
            browser.should(have.url_containing(f'/#/article/{url_title}'))
        with step('Checking the title'):
            s('.banner h1').should(have.text(article["title"]))
        with step('Checking body'):
            s('[ng-bind-html$=body]').should(have.text(article["body"]))
        with step('Checking the tags'):
            self.checking_tags(article)
        return self

    def check_subscription(self):
        follow_button = s('.banner .article-meta [user$="article.author"] button')
        if follow_button.perform(command.js.scroll_into_view).matching(have.text('Unfollow')):
            follow_button.click()
        follow_button.perform(command.js.scroll_into_view).should(have.text('Follow')).click()
        return self
