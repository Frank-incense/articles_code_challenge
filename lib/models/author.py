from db.connection import db_conn,db_cursor
from db.schema import authors

class Author:
    all = {}
    def __init__(self, name, email):
        self.id = None
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<Author {self.id}: {self.name}: {self.email}>"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name should be a string")
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if isinstance(email, str) and len(email) > 0:
            self._email = email
        else:
            raise ValueError("Email should be a string")

    @classmethod
    def create_table(cls):
        db_cursor.execute(authors)
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
            INSERT INTO authors(name, email)
            VALUES (?,?)
        """
        db_cursor.execute(sql, (self.name,self.email))
        db_conn.commit()

        self.id = db_cursor.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, email):
        author = cls( name, email)
        author.save()
        return author

    def update(self):
        sql = """
            UPDATE authors
            SET name = ?, email = ?
            WHERE id = ?
        """
        db_cursor.execute(sql, (self.name, self.email, self.id))
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
            author.email = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            author = cls(row[1], row[2])
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
            WHERE name is ?
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
                                 magazine_id=magazine,
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