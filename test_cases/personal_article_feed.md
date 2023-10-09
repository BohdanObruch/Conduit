Personal article feed test case

# This should display the user's subscription to others and display articles in the Your Feed tab:

## Before

1. Open https://demo.realworld.io/
2. Repeat steps 2-9 from [login user](/test_cases/login_user.md)
3. Url should be `/#/` — main page

## Open random article

4. Click **Global Feed** in feed toggle menu
5. Select **random article** from list
6. Url should be `/#/article/{article_slug}`

## Follow author

7. Click button **Follow**
8. Confirm that the button text changes to **Unfollow**

## Check user in your subscription list

9. Click **Home**
10. In feed toggle menu should be active **Your Feed**
11. Check `{authorFollowed}` should be visible

## Where:

- `{authorFollow}` — subscribed author
- `{article_slug}` - random article slug