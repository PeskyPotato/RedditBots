'''
Grabs submission from a given subreddit over a fixed interval and tweets the
set amount of posts. The tweets are recorded in a database to prevent
tweeting duplicate posts. A delay is added to avoid spamming twitter.
'''

import praw
import tweepy
from tweepy import OAuthHandler
import time
import sqlite3

'''
CONFIG INFORMATION
==================
This variables below can be put in a separate file but I've decided to keep
this all in one.
'''
SUB = ''                # Enter the subredit you want to monitor
INTERVAL = 900          # Interval you want the script to run, default 900 seconds
POST_LIMIT = 10         # Number of posts you want to grab each time

# Reddit recdential go below
reddit = praw.Reddit(client_id = '',
                     client_secret= '',
                     user_agent= 'Tweets hot posts on Twitter by /u/')

# Twitter credentials go below
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

'''
FUNCTIONS
=========
Below are all the functions that the script needs to run.
'''

'''
Shortens titles greater than 250 characters and adds ellipses.
'''
def strip_title(title):
	if len(title) < 250:
		return title
	else:
		return title[:249] + "..."

'''
This function gets the posts from Reddit, records them in the database and
sends them over to tweeter() in a list to tweet.
'''
def poster():
    # Creates conneciton to the database
    conn = sqlite3.connect('posted_id.db')
    c = conn.cursor()
    toTweet = []
    for submission in reddit.subreddit(SUB).hot(limit=POST_LIMIT):
        if not submission.stickied:     # Checks if post is stickied
            url = submission.shortlink
            title = strip_title(submission.title)
            udate = time.strftime("%Y-%m-%d %X",time.gmtime(submission.created_utc))

            try:
                # This keeps a record of the posts in a the database
                c.execute("INSERT INTO posts (id, title, udate) VALUES (?, ?, ?)",
                (url, title, udate))
                conn.commit()

                message = title + " " + url
                #print(message)
                toTweet.append(message)

            except sqlite3.IntegrityError:
                # This means the post was already tweeted and is ignored
                #print("Duplicate", url)
                pass

    c.close()
    conn.close()
    tweeter(toTweet)

'''
This tweets all the posts found by poster() with a 60 second delay between
each one to avoid spamming tweets out. The delay can be adjusted by changing
time.sleep(60).
'''
def tweeter(toTweet):
    for message in toTweet:
        #api.update_status(status = message)
        print("Tweeted: " + message)
        time.sleep(60)

'''
Creates the table in `posted_id.db`, if a table already exists this is ignored.
'''
def create_table():
    conn = sqlite3.connect('posted_id.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (id TEXT NOT NULL UNIQUE, title TEXT, udate TEXT, PRIMARY KEY (id))')
    c.close()
    conn.close()

'''
This runs the program in a loop infinitly.
'''
def main():
    while True:
        poster()
        print("Sleeping")
        time.sleep(INTERVAL)

if __name__ == '__main__':
    create_table()
    main()
