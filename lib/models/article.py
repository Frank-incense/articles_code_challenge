from db import db_conn,db_cursor
from db.schema import articles

class Article:

    all = {}

    def __init__(self, author_id, magazine_id, title):
       self.id = None
       self.author_id = author_id
       self.magazine_id = magazine_id
       self.title = title

    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"
    @property
    def author_id(self):
        return self._author_id
    
    @author_id.setter
    def author_id(self, author_id):
        from .author import Author
        if Author.find_by_id(author_id):
            self._author_id = author_id
        else:
            raise ValueError("Author id should of an author")
    
    @property
    def magazine_id(self):
        return self._magazine_id
    
    @magazine_id.setter
    def magazine_id(self, magazine_id):
        from .magazine import Magazine
        if Magazine.find_by_id(magazine_id):
            self._magazine_id = magazine_id
        else:
            raise ValueError("Magazine id should of an magazine")
    
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, title):
        if isinstance(title, str) and len(title) > 0:
            self._title = title
        else:
            raise ValueError("Title should not be an empty string")
    
    
    @classmethod
    def create_table(cls):
        db_cursor.execute(articles)
        db_conn.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS articles;
        """
        db_cursor.execute(sql)
        db_conn.commit()
    
    def save(self):
        sql = """
            INSERT INTO articles(author_id, magazine_id, title)
            VALUES (?,?,?)
        """
        db_cursor.execute(sql, (self.author_id,
                                self.magazine_id,
                                self.title))
        db_conn.commit()

        self.id = db_cursor.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, author_id, magazine_id, title):
        article = cls(author_id, magazine_id, title)
        article.save()
        return article

    def update(self):
        sql = """
            UPDATE articles
            SET author_id = ?, magazine_id = ?, title = ?
            WHERE id = ?
        """
        db_cursor.execute(sql, (self.author_id,
                                self.magazine_id,
                                self.title, 
                                self.id))
        db_conn.commit()

    def delete(self):
        sql = """
            DELETE FROM articles
            WHERE id = ?
        """

        db_cursor.execute(sql, (self.id,))
        db_conn.commit()

        del type(self).all[self.id]
        self.id = None
        
    @classmethod
    def instance_from_db(cls, row):
        article = cls.all.get(row[0])
        if article:
            # ensure attributes match row values in case local object was modified
            article.author_id = row[1]
            article.magazine_id = row[2]
            article.title = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            article = cls(row[1], row[2], row[3], row[4])
            article.id = row[0]
            cls.all[article.id] = article
        return article

    @classmethod
    def get_all(cls):
        """Return a list containing a article object per row in the table"""
        sql = """
            SELECT *
            FROM articles
        """

        rows = db_cursor.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a article object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM articles
            WHERE id = ?
        """

        row = db_cursor.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_title(cls, title):
        """Return a article object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM articles
            WHERE title is ?
        """

        row = db_cursor.execute(sql, (title,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    