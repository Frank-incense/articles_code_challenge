from connection import db_cursor, db_conn
from schema import articles, authors, magazines
from models.author import Author
from models.magazine import Magazine
from models.article import Article
from faker import Faker

def seed_data():
    # Drop existing tables (optional for dev)
    db_cursor.execute("DROP TABLE IF EXISTS authors")
    db_cursor.execute("DROP TABLE IF EXISTS magazines")
    db_cursor.execute("DROP TABLE IF EXISTS articles")

    # Create tables
    db_cursor.execute(authors)
    db_cursor.execute(magazines)
    db_cursor.execute(articles)

    # Create and insert data
    
    # author1 = Author("Nancy")
    # author1.save()

    # author2 = Author("Brian")
    # author2.save()

    # mag1 = Magazine("Tech Today", "Technology")
    # mag1.save()

    # mag2 = Magazine("Health Monthly", "Health")
    # mag2.save()

    # art1 = Article("The Future of AI", "AI is evolving fast.", author1, mag1)
    # art1.save()

    # art2 = Article("Healthy Eating", "Start your day with fruit.", author2, mag2)
    # art2.save()

    # print("✅ Seed data inserted successfully.")

    # conn.commit()
    # conn.close()
