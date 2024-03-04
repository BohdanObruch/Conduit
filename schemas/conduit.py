from voluptuous import Schema, Any, ALLOW_EXTRA, PREVENT_EXTRA

user = Schema({
    "user": {
        "id": int,
        "email": str,
        "username": str,
        "bio": Any(None, str),
        "image": str,
        "token": str
    }
})

tags = Schema({
    "tags": [str]
})

articles = Schema({
    "article": {
        "id": int,
        "slug": str,
        "title": str,
        "description": str,
        "body": str,
        "createdAt": str,
        "updatedAt": str,
        "authorId": int,
        "tagList": [
            str
        ],
        "author": {
            "username": str,
            "bio": Any(None, str),
            "image": str,
            "following": bool
        },
        "favoritedBy": [
            {
                "id": int,
                "email": str,
                "username": str,
                "password": str,
                "image": str,
                "bio": Any(None, str),
                "demo": bool
            }
        ],
        "favorited": bool,
        "favoritesCount": int
    }
})

comments = Schema({
    "comments": [
        {
            "id": int,
            "createdAt": str,
            "updatedAt": str,
            "body": str,
            "author": {
                "username": str,
                "bio": Any(None, str),
                "image": str,
                "following": bool
            }
        }
    ]
})

add_comment = Schema({
    "comment": {
        "id": int,
        "createdAt": str,
        "updatedAt": str,
        "body": str,
        "author": {
            "username": str,
            "bio": Any(None, str),
            "image": str,
            "following": bool
        }
    }
})

profile = Schema({
    "profile": {
        "username": str,
        "bio": Any(None, str),
        "image": str,
        "following": bool
    }
})

articles_follow_and_global = Schema({
    "articles": [
        {
            "slug": str,
            "title": str,
            "description": str,
            "body": str,
            "tagList": [str],
            "createdAt": str,
            "updatedAt": str,
            "favorited": bool,
            "favoritesCount": int,
            "author": {
                "username": str,
                "bio": Any(None, str),
                "image": str,
                "following": bool
            }
        }
    ],
    "articlesCount": int
})

article = Schema({
    "article": {
        "slug": str,
        "title": str,
        "description": str,
        "body": str,
        "tagList": [str],
        "createdAt": str,
        "updatedAt": str,
        "favorited": bool,
        "favoritesCount": int,
        "author": {
            "username": str,
            "bio": Any(None, str),
            "image": str,
            "following": bool
        }
    }
})
