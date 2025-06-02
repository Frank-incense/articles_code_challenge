import sqlite3

def get_connection():
    db_conn = sqlite3.connect('code_challenge.db')
    return db_conn