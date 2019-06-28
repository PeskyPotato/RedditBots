'''
Replies to comments based on keywords with predefined responses. 
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

def date_print(message):
    '''Prints messages with date'''
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)

def createTable():
'''Creates a database file and table if one does not already exist.'''

    conn = sqlite3.connect('posted.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (perma TEXT NOT NULL UNIQUE, author TEXT, PRIMARY KEY (perma))')
    c.close()
    conn.close()

def dbWrite(perma, author):
'''Writes comments to table, if the comment exists returns a 0 else returns a 1.'''
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
'''Gets random responses'''
    return random.choice(RESPONSES)

def checkSubmissions():
'''Checks for submissions and then replies'''
    for submission in reddit.subreddit(SUBREDDIT).hot(limit=SUBMISSION_LIMIT):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            for keyword in KEYWORDS:
                if keyword.lower() in comment.body.lower():
                    response = getResponse()
                    if response and dbWrite(comment.id, comment.author):
                        comment.reply(response)
                        date_print("Replied to {} with {}".format(comment.id, response.strip()))


def main():
    createTable()
    while(1):
        checkSubmissions()
        date_print("Sleeping for {} seconds".format(SLEEP_TIME))
        sleep(SLEEP_TIME)

main()