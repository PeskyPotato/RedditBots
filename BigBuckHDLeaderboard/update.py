'''
Posts daily standings for Main Skill from BigBuckHD onto /r/BigBuckHunter
'''
import requests
import json
from datetime import datetime
import sqlite3
import praw

conn = sqlite3.connect('standings.db')

reddit = praw.Reddit(client_id='',
                    client_secret='',
                    user_agent='Post game rankings to r/BigBuckHunter/ by u/PeskyPotato',
                    refresh_token='',
                    redirect_uri='https://127.0.0.1:70000')

post = ''

def createTable():
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS standings (id TEXT NOT NULL UNIQUE, name TEXT, rank INTEGER, prev_rank_hour INTEGER, prev_rank_day INTEGER, date_hour TEXT, date_day TEXT, PRIMARY KEY (id))')

def dbWrite(id, name, rank, prev_rank_hour, prev_rank_day, date_hour, date_day):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO standings (id, name, rank, prev_rank_hour, prev_rank_day, date_hour, date_day) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (id, name, rank, prev_rank_hour, prev_rank_day, date_hour, date_day))
        conn.commit()
    except sqlite3.IntegrityError:
        return 0

    return 1

def dbSelect(id):
    c = conn.cursor()
    c.execute("SELECT * FROM standings WHERE id=?", (id,))
    row = c.fetchone()
    return row

def dbUpdate(entries):
    c = conn.cursor()
    c.execute("UPDATE standings SET rank = ?, prev_rank_hour = ?, prev_rank_day = ?, date_hour = ?, date_day = ? WHERE id = ?", entries)
    conn.commit()

def dbOrder():
    c = conn.cursor()
    c.execute("SELECT * FROM standings ORDER BY rank ASC")
    rows = c.fetchall()
    return rows


def updateTable():
    r = requests.get('https://www.bigbuckhd.com/world/qualifiers_search?order_by=SkillRank&order_direction=desc&limit=100&offset=0')
    data = r.json()

    createTable()
    post_trigger = False
    for user in data:
        row = dbSelect(user['id'])
        if not row:
            dbWrite(user['id'], user['name'], user['overall_rank'], user['overall_rank'], user['overall_rank'], user['update_time'], user['update_time'])
            row = dbSelect(user['id'])

        # daily change
        data_time = datetime.strptime(user['update_time'], '%Y-%m-%d %H:%M:%S')
        u_time = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
        delta = data_time - u_time
        print(row[1], delta, delta.seconds)
        # if delta.seconds > 3600:
        if delta.days > 0:
            row = dbSelect(user['id'])
            rank_change = row[4] - row[2]
            prev_rank = row[2]
            dbUpdate((user['overall_rank'], row[3], prev_rank, row[5], user['update_time'], user['id']))
            print(user['name'], user['overall_rank'])
            post_trigger = True
    if post_trigger:
        createPost()

def createPost():
    body = "{}\n\nName|Rank Today|Yesterday|Rank Change (daily)\n:--:|:--:|:--:|:--:".format(datetime.utcnow().strftime("Last Updated on %d %B %Y at %H:%M:%S"))
    for user in dbOrder()[:100]:
        rank_change_hour = user[4] - user[2]
        if rank_change_hour > 0:
            rank_change_s = "+{}".format(rank_change_hour)
        elif rank_change_hour < 0:
            rank_change_s = str(rank_change_hour)
        else:
            rank_change_s = "0"
        body += "\n{}|{}|{}|{}".format(user[1], user[2], user[4], rank_change_s)
    print(body)
    title = 'Leaderboard Update (Main Skill)'
    post = reddit.submission(id='cw804i')
    post.edit(body)
    # reddit.subreddit('BigBuckHunter').submit(title, selftext=body)

def main():
    updateTable()

main()
