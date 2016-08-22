import sqlite3

def init_db(out_db):
    out_c = out_db.cursor()
    out_c.execute('''CREATE TABLE IF NOT EXISTS imgs
        (link TEXT PRIMARY KEY,
        tag TEXT,
        FOREIGN KEY(tag) REFERENCES tags(tag))''')
    out_c.execute('''CREATE TABLE IF NOT EXISTS tags
        (tag TEXT PRIMARY KEY,
        related TEXT)''')
    out_db.commit()