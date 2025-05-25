import sqlite3

db_conn = sqlite3.connect('db/articles.db')
db_cursor = db_conn.cursor()