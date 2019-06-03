'''
Gets the top clips from the last 24 hours/7 days/30 days/all time from a 
twich streamer and posts them to the targetted subreddit, if the bot has
not already posted them before. The bot is setup to run daily at the 
user specified time.

The number of top clips that can be retrieved as well as the order 
based on popularity or trending can be set in config.json, along 
with all the other parameters and API credentials.
'''

import requests
import json
import sqlite3
import praw
from time import sleep, strftime
from datetime import datetime
import schedule

with open('config.json', 'r') as f:
    config_data = json.load(f)

reddit = praw.Reddit(client_id=config_data["reddit_client_id"],
                     client_secret=config_data["reddit_client_secret"],
                     username=config_data["reddit_username"],
                     password=config_data["reddit_password"],
                     user_agent='Posts clips from twitch, test by /u/PeskyPotato')

TIME = config_data["time"]
SUB = config_data["subreddit"]
TWTICH_USER = config_data["twitch_user"]
PERIOD = config_data["twitch_period"]
TRENDING = config_data["twitch_trending"]
LIMIT = config_data["twitch_limit"]

'''
Creates a database file and table if one does not already exist.
'''
def createTable():
    conn = sqlite3.connect('posted.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (slug TEXT NOT NULL UNIQUE, title TEXT, udate TEXT, author TEXT, PRIMARY KEY (slug))')
    c.close()
    conn.close()

'''
Writes post to table, if the post exists returns a 0 if succesfully returns a 1.
'''
def dbWrite(slug, title, udate, author):
    try:
        conn = sqlite3.connect('posted.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (slug, title, udate, author) VALUES (?, ?, ?, ?)", (slug, title, udate, author))
        conn.commit()
    except sqlite3.IntegrityError:
        c.close()
        conn.close()
        return 0

    c.close()
    conn.close()
    return 1

'''
Posts the clip to the specified subreddit, handles exceeding rate limit by
sleeping for 15 minutes.
'''
def postSub(url, title):
    try:
        reddit.subreddit(SUB).submit(title, url=url)
    except praw.exceptions.APIException:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Rate limited, sleeping for 15 minutes")
        sleep(900)
        reddit.subreddit(SUB).submit(title, url=url)
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Posted", title)
    sleep(10)


'''
Gets top 50 trending clips from the last 7 days from specified twitch user. Then 
passes the url and title of the clip to postSub if not in the database.
'''
def checkClips():
    url = "https://api.twitch.tv/kraken/clips/top?channel={}&period={}&trending={}&limit={}".format(TWTICH_USER, PERIOD, TRENDING, LIMIT)
    headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': config_data["twitch_client_id"]}
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        data = r.json()
    else:
        print("Invalid request", r.status_code)
        r.raise_for_status()

    for clip in data["clips"]:
        if dbWrite(clip["slug"], clip["title"], clip["created_at"], clip["curator"]["id"]):
            postSub(clip["url"], clip["title"])


def main():
    createTable()
    checkClips()

schedule.every().day.at(TIME).do(main)
while True:
    schedule.run_pending()
    sleep(1)
