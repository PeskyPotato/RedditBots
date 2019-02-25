'''
Adds new users to a database and prints out the new users each time
the script is run. A user is determined to be 'new' if their username
does ntnoto appear in the database. The usernames are gathered from 
submission and comment authors.
'''
import praw
import sqlite3

reddit = praw.Reddit(client_id = '',
                     client_secret= '',
                     user_agent= 'Grabs new users from a sub by /u/PeskyPotato')

SUB = 'RequestABot'
new_users = []

def grabber():
    for submission in reddit.subreddit(SUB).new(limit = 1000):
        if dbWrite(submission.author):
            new_users.append(str(submission.author))
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if dbWrite(comment.author):
                new_users.append(str(comment.author))

def createTable():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (user TEXT NOT NULL UNIQUE, PRIMARY KEY (user))')
    c.close()
    conn.close()

def dbWrite(user):
    user = str(user)
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (user) VALUEs (?)", (user,))
        conn.commit()
    except sqlite3.IntegrityError:
        c.close()
        conn.close()
        return 0

    c.close()
    conn.close()
    return 1

createTable()
grabber()
for user in new_users:
    print(user)
