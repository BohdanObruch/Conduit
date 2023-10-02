Edit Settings in test case

# It should do edit setting user:

## Before

1. Open https://demo.realworld.io/
2. Repeat steps 2-9 from [login user](/test_cases/login_user.md)
3. Url should be `/#/` — main page

## Open settings form

4. Click **Settings** link in app header
5. Url should be `/#/settings`
6. Page heading should be **Your Settings**

## Edit settings

7. Page should have form
8. Clear all forms fields
9. Insert `{new_picture_url}` into **URL of profile picture** form field
10. Type `{new_username}` into **Username** form field
11. Type `{new_bio}` into **Short bio about you** form field
12. Type `{new_email}` into **Email** form field

## Submit form

13. Click on **Update Settings** button

## Check updated settings

14. Redirect to main page
15. Url should be `/#/@{new_username}`
16. Header and user-info block should contains `{new_username}`
17. User-info block should contains `{new_bio}`
18. Header should contains `{new_picture}`

# Where:

* `{new_email}`
    * valid email
    * was not registered before
* `{new_picture_url}`
    * valid url to image
    * image should be accessible
* `{new_username}`
    * string with length from 3 to 20 chars
    * was not registered before
* `{new_bio}`
    * string with length from 20 to 100 chars
