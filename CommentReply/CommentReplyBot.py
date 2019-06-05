'''
Replies to comments based on keywords with predefined
responses. 
'''

import praw
from time import sleep, strftime
from datetime import datetime
import sqlite3
import random

# Reddit API credentials
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='Replies to comments based on keywords')

SLEEP_TIME = 60
SUBREDDIT = 'test'
KEYWORDS = ['test', 'test2', 'a keyword']
SUBMISSION_LIMIT = 20
with open('responses.txt') as f:
    RESPONSES = list(f)

'''
Creates a database file and table if one does not already exist.
'''
def createTable():
    conn = sqlite3.connect('posted.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (perma TEXT NOT NULL UNIQUE, author TEXT, PRIMARY KEY (perma))')
    c.close()
    conn.close()

'''
Writes comments to table, if the comment exists returns a 0 if succesfully returns a 1.
'''
def dbWrite(perma, author):
    try:
        conn = sqlite3.connect('posted.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (perma, author) VALUES (?, ?)", (perma, str(author)))
        conn.commit()
    except sqlite3.IntegrityError:
        c.close()
        conn.close()
        return 0

    c.close()
    conn.close()
    return 1

def getResponse():
    return random.choice(RESPONSES)

def checkSubmissions():
    for submission in reddit.subreddit(SUBREDDIT).hot(limit=SUBMISSION_LIMIT):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            for keyword in KEYWORDS:
                if keyword.lower() in comment.body.lower():
                    response = getResponse()
                    if response and dbWrite(comment.id, comment.author):
                        comment.reply(response)
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "replied to", comment.id, "with", response.strip())                    
        

def main():
    while(1):
        createTable()
        checkSubmissions()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "sleeping for", SLEEP_TIME, "seconds")
        sleep(SLEEP_TIME)

main()