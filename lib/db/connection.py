import sqlite3
def get_connection():
    db_conn = sqlite3.connect('code_challenge.db')
    db_conn.row_factory = sqlite3.Row
    return db_conn