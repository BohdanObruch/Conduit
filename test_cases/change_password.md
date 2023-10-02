Change Password in test case

# It should do change password user:

## Before

1. Open https://demo.realworld.io/
2. Repeat steps 2-9 from [login user](/test_cases/login_user.md)
3. Url should be `/#/` — main page

## Open settings form

4. Repeat steps 4-7 from [edit settings](/test_cases/edit_settings.md)

## Edit settings

5. Type `{new_password}` into **New Password** form field

## Submit form

6. Click on **Update Settings** button

## Check updated settings

7. Redirect to main page
8. Url should be `/#/@{username}`
9. Header and user-info block should contains `{username}`

# Where:

* `{new_password}` — new user password
    * string with pattern `[0-9a-zA-Z_]{6, 16}`

