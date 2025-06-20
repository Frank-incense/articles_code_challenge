from lib.db.connection import get_connection

db_conn = get_connection()
db_cursor = db_conn.cursor()

class Author:
    all = {}
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name should be a string")
    

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS authors(
        id INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL
        )"""
        db_cursor.execute(sql)
        db_conn.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS authors;
        """
        db_cursor.execute(sql)
        db_conn.commit()
    
    def save(self):
        sql = """
            INSERT INTO authors(name)
            VALUES (?)
        """
        db_cursor.execute(sql, (self.name,))
        db_conn.commit()

        self.id = db_cursor.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name):
        author = cls( name)
        author.save()
        return author

    def update(self):
        sql = """
            UPDATE authors
            SET name = ?
            WHERE id = ?
        """
        db_cursor.execute(sql, (self.name, self.id))
        db_conn.commit()

    def delete(self):
        sql = """
            DELETE FROM authors
            WHERE id = ?
        """

        db_cursor.execute(sql, (self.id,))
        db_conn.commit()

        del type(self).all[self.id]
        self.id = None
        
    @classmethod
    def instance_from_db(cls, row):
        author = cls.all.get(row[0])
        if author:
            # ensure attributes match row values in case local object was modified
            author.name= row[1]
        else:
            # not in dictionary, create new instance and add to dictionary
            author = cls(row[1])
            author.id = row[0]
            cls.all[author.id] = author
        return author

    @classmethod
    def get_all(cls):
        """Return a list containing a author object per row in the table"""
        sql = """
            SELECT *
            FROM authors
        """

        rows = db_cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]if rows else None

    @classmethod
    def find_by_id(cls, id):
        """Return a author object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM authors
            WHERE id = ?
        """

        row = db_cursor.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return an author object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM authors
            WHERE name = ?
        """

        row = db_cursor.execute(sql, (name,)).fetchone()
        
        return cls.instance_from_db(row) if row else None
    
    def articles(self):
        from .article import Article
        sql = """
            SELECT *
            FROM articles
            WHERE author_id = ?"""
        rows = db_cursor.execute(sql, (self.id,)).fetchall()
        return [Article.instance_from_db(row) for row in rows] if rows else None

    
    def magazines(self):
        from .magazine import Magazine
        sql = """
            SELECT DISTINCT
            articles.magazine_id AS id, 
            magazines.name AS name, 
            magazines.category AS category
            FROM articles
            INNER JOIN authors
            ON articles.author_id = authors.id
            INNER JOIN magazines
            ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?"""
        rows = db_cursor.execute(sql, (self.id,)).fetchall()
        return [Magazine.instance_from_db(row) for row in rows] if rows else None

    def add_article(self, magazine, title):
        from .article import Article
        try:
            newArticle = Article.create(author_id=self.id, 
                                 magazine_id=magazine.id,
                                 title=title)
            print(f"Success: new article {newArticle} has been created")
        except ValueError as e:
            print(f"Error creating: {e}")

    def topic_areas(self):
        sql = """
            SELECT DISTINCT 
            magazines.category AS category
            FROM articles
            INNER JOIN authors
            ON articles.author_id = authors.id
            INNER JOIN magazines
            ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?"""
        rows = db_cursor.execute(sql, (self.id,)).fetchall()
        return [row[0] for row in rows] if rows else None
    
    @classmethod
    def top_author(cls):
        sql = """
            SELECT DISTINCT
            articles.author_id,
            authors.name,
            COUNT(articles.id) as articles
            FROM articles
            INNER JOIN authors
            ON articles.author_id = authors.id
            GROUP BY articles.author_id
            ORDER BY articles DESC
        """

        row = db_cursor.execute(sql).fetchone()
        return cls.instance_from_db(row) if row else None