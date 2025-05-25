from db import db_conn,db_cursor
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
            magazine.author_id = row[1]
            magazine.magazine_id = row[2]
            magazine.title = row[3]
            magazine.content = row[4]
        else:
            # not in dictionary, create new instance and add to dictionary
            magazine = cls(row[1], row[2], row[3], row[4])
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
    def find_by_name(cls, category):
        sql = """
            SELECT *
            FROM magazines
            WHERE category is ?
        """

        rows = db_cursor.execute(sql, (category,)).fetchall()
        return [cls.instance_from_db(row) for row in rows] if rows else None
    
    def authors_with_articles(self):
        sql = """
            SELECT articles.title, authors.name
            FROM articles
            INNER JOIN authors
            ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
        """
        rows = db_cursor.execute(sql, (self.id,))
        return [print(row) for row in rows]
