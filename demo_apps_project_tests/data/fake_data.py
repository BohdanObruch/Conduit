import random
from faker import Faker
fake = Faker()


def generate_random_user_data():
    user_data = {
        "username": f'{random.randint(1, 100)}{fake.user_name()}',
        "email": f'{random.randint(1, 100)}{fake.email()}',
        "password": fake.password(),
        "picture": fake.image_url(),
        "bio": fake.text()
    }
    return user_data


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
