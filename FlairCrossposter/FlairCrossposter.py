'''
Crossposts a submission with a specific flair to a
targeted subreddit. The post is saved in a database
and checked to make sure it is not posted twice.
'''
import praw
from time import sleep, strftime
from datetime import datetime
import sqlite3

# Reddit API credentials
reddit = praw.Reddit(client_id='',
                    client_secret='',
                    username='',
                    password='',
                     user_agent='Crosspost specific flaired posts by /u/PeskyPotato')

# Change parameters 
subR = "datahoarder"           # subreddit to check the flair on, enter without "/r/"
sub_cross = "test"      # subreddit to crosspost to, enter without "/r/"
flair = "Ohh Yeah!"     # the text of the flair to look for
sleep_time = 120        # time to sleep between each cycle in seconds, default 120 seconds.

'''
Creates a database file and table if one does not already exist.
'''
def createTable():
    conn = sqlite3.connect('posted.db')
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
        conn = sqlite3.connect('posted.db')
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

def grabber(subR):
    for submission in reddit.subreddit(subR).hot(limit=100):
        sub_flair = submission.link_flair_text
        if sub_flair == flair and dbWrite(submission.permalink, submission.title, submission.created, submission.author):
            try:
                submission.crosspost(sub_cross, submission.title)
                print("Crossposted", submission.title)

            except praw.exceptions.APIException:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "You are doing too much, trying to post again in 15 minutes")
                time.sleep(900)
                try:
                    submission.crosspost(sub_cross, submission.title)
                    print("Crossposted", submission.title)
                except praw.exceptions.APIException as e:
                    print("Error posting", submission.title)
                    with ("errors.log", "a+") as f:
                        f.write(e)
                        f.write(submission.permalink)

if __name__ == '__main__':
    createTable()
    while True:
        grabber(subR)
        print("Sleeping for", sleep_time, "seconds")
        sleep(sleep_time)