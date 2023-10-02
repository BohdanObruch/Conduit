from faker import Faker

fake = Faker()


def generate_random_user_data():
    user_name = fake.user_name()
    user_email = fake.email()
    user_password = fake.password()
    user_picture = fake.image_url()
    user_bio = fake.text()
    return user_name, user_email, user_password, user_picture, user_bio


username = generate_random_user_data()[0]
email = generate_random_user_data()[1]
password = generate_random_user_data()[2]
picture = generate_random_user_data()[3]
bio = generate_random_user_data()[4]


def generate_random_article_data():
    title = fake.word()
    description = fake.text()
    body = fake.text()
    tags = []
    for _ in range(5):
        tags.append(fake.word())
    return title, description, body, tags


title_article = generate_random_article_data()[0]
description_article = generate_random_article_data()[1]
body_article = generate_random_article_data()[2]
tags_article = generate_random_article_data()[3]
