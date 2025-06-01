from db.connection import db_conn,db_cursor
from db.schema import magazines

class Magazine:

    all = {}
    def __init__(self, name, category):
        self.id = None
        self.name = name
        self.category = category
        
    def __repr__(self):
        return f"<Magazine {self.id}: {self.name}: {self.category}>"
    
    @classmethod
    def create_table(cls):
        db_cursor.execute(magazines)
        db_conn.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS magazines;
        """
        db_cursor.execute(sql)
        db_conn.commit()
    
    def save(self):
        sql = """
            INSERT INTO magazines(name, category)
            VALUES (?,?)
        """
        db_cursor.execute(sql, (self.name,self.category))
        db_conn.commit()

        self.id = db_cursor.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, category):
        magazine = cls( name, category)
        magazine.save()
        return magazine

    def update(self):
        sql = """
            UPDATE magazines
            SET name = ?, category = ?
            WHERE id = ?
        """
        db_cursor.execute(sql, (self.name, self.category, self.id))
        db_conn.commit()

    def delete(self):
        sql = """
            DELETE FROM magazines
            WHERE id = ?
        """

        db_cursor.execute(sql, (self.id,))
        db_conn.commit()

        del type(self).all[self.id]
        self.id = None
        
    @classmethod
    def instance_from_db(cls, row):
        magazine = cls.all.get(row[0])
        if magazine:
            # ensure attributes match row values in case local object was modified
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            magazine = cls(row[1], row[2])
            magazine.id = row[0]
            cls.all[magazine.id] = magazine
        return magazine

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM magazines
        """

        rows = db_cursor.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM magazines
            WHERE id = ?
        """

        row = db_cursor.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM magazines
            WHERE name is ?
        """

        row = db_cursor.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_category(cls, category):
        sql = """
            SELECT *
            FROM magazines
            WHERE category is ?
        """

        rows = db_cursor.execute(sql, (category,)).fetchall()
        return [cls.instance_from_db(row) for row in rows] if rows else None
    
    def articles(self):
        from .article import Article
        sql = """
            SELECT articles.id,
            articles.author_id,
            magazines.id,
            articles.title
            FROM articles
            JOIN magazines
            ON articles.magazine_id = magazines.id
            WHERE magazine_id = ?"""
        rows = db_cursor.execute(sql, (self.id,)).fetchall()
        return [Article.instance_from_db(row) for row in rows] if rows else None

    def contributors(self):
        from .author import Author
        sql = """
            SELECT DISTINCT articles.author_id, authors.name, authors.email
            FROM articles
            INNER JOIN authors
            ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
        """
        rows = db_cursor.execute(sql, (self.id,))
        return [Author.instance_from_db(row) for row in rows] if rows else None
    
    def count_articles(self):
        sql = """
            SELECT 
            COUNT(articles.id) AS articles
            FROM articles
            INNER JOIN magazines
            ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        """
        count = db_cursor.execute(sql, (self.id,)).fetchone
        return count[0]
    
    @classmethod
    def most_contributions(cls):
        from .author import Author
        sql = """
            SELECT 
            author_id, 
            count(id) as contributions
            FROM articles
            GROUP BY author_id
            ORDER BY contributions DESC
        """
        author = db_cursor.execute(sql).fetchone()
        return Author.find_by_id(author[0]) if author else None
    
    def article_titles(self):
        sql = """
            SELECT title 
            FROM articles
            WHERE magazine_id = ?
        """

        titles = db_cursor.execute(sql, (self.id,)).fetchall()
        return [title[0] for title in titles]if titles else None
    
    def contributing_authors(self):
        from .author import Author
        sql = """
            SELECT 
            authors.id,
            authors.name,
            authors.email
            FROM articles
            INNER JOIN authors
            ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY articles.author_id
            HAVING COUNT(articles.id) > 1
        """
        authors = db_cursor.execute(sql, (self.id,))
        return [Author.instance_from_db(author) for author in authors]if authors else None