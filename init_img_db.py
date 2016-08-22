import sqlite3

def init_img_db(out_db):
    print("STARTING IMAGE SEARCH, PLEASE WAIT")
    out_c = out_db.cursor()
    out_c.execute('''CREATE TABLE IF NOT EXISTS imgs
        (link TEXT PRIMARY KEY,
        tag TEXT,
        FOREIGN KEY(tag) REFERENCES tags(tag))''')
    out_c.execute('''CREATE TABLE IF NOT EXISTS tags
        (tag TEXT PRIMARY KEY,
        related TEXT)''')
    out_c.execute('''CREATE TABLE IF NOT EXISTS related_tags
        (source TEXT,
        target TEXT,
        PRIMARY KEY(source, target),
        FOREIGN KEY(source) REFERENCES tags(tag),
        FOREIGN KEY(target) REFERENCES tags(tag))''')
    out_db.commit()