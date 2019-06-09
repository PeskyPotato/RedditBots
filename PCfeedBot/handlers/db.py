import sqlite3

'''
Creates a database file and table if one does not already exist.
'''
def createTable():
    conn = sqlite3.connect('replied.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (perma TEXT NOT NULL UNIQUE, title TEXT, udate TEXT, author TEXT, PRIMARY KEY (perma))')
    c.close()
    conn.close()

'''
Writes post to table, if the post exists
returns a 0 if succesfully returns a 1.
'''
def dbWrite(perma, title, udate, author):
    try:
        conn = sqlite3.connect('replied.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (perma, title, udate, author) VALUES (?, ?, ?, ?)", (perma, title, udate, str(author)))
        conn.commit()
    except sqlite3.IntegrityError:
        c.close()
        conn.close()
        return 0

    c.close()
    conn.close()
    return 1
