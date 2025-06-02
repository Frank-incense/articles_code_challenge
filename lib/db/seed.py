from models.author import Author
from models.magazine import Magazine
from models.article import Article
from faker import Faker

import random

def seed_data():
    # Drop tables
    Magazine.drop_table()
    Author.drop_table()
    Article.drop_table()
    # Create tables
    Magazine.create_table()
    Author.create_table()
    Article.create_table()

    fake = Faker()
    # Create and insert data
    authors = [Author.create(
                        name=fake.name(),
                        ) 
               for i in range(20)]
    magazines = [Magazine.create(
                    name=fake.company(),
                    category=random.choice(["Techonology", "Lifestyle", "Business", "Health"])
                    )
                 for i in range(10)]
   

    articles = [Article.create(
                            author_id=random.choice(authors).id,
                            magazine_id=random.choice(magazines).id,
                            title=fake.catch_phrase()
                            ) 
                            for i in range(100)]

    print("✅ Seed data inserted successfully.")
