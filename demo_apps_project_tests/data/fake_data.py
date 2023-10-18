import random
from faker import Faker
fake = Faker()


def generate_random_user_data():
    user_data = {
        "username": fake.user_name(),
        "email": f'{random.randint(1, 100)}{fake.email()}',
        "password": fake.password(),
        "picture": fake.image_url(),
        "bio": fake.text()
    }
    return user_data


# user_data = generate_random_user_data()
# username = user_data["username"]
# email = user_data["email"]
# password = user_data["password"]


def generate_random_article():
    article_data = {
        "title": fake.text(max_nb_chars=80),
        "description": fake.paragraph(),
        "body": fake.paragraph(),
        "tags": [],
        "comments": fake.paragraph()
    }
    num_tags = random.randint(1, 5)
    for _ in range(num_tags):
        article_data["tags"].append(fake.word())
    return article_data


# article_data = generate_random_article()
# title_article = article_data["title"]
# description_article = article_data["description"]
# body_article = article_data["body"]
# tags_article = article_data["tags"]
