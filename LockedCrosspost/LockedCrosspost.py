'''
Gets posts from /r/all sorted by hot, if post is not locked, not NSFW
and not in the table, it posts to the specified subreddit.
'''
import praw
from time import sleep, strftime
from datetime import datetime
import sqlite3

'''
Initialise Reddit
Enter user credentials
''' 
reddit = praw.Reddit(client_id='',
                    client_secret='',
                    username='',
                    password='',
                    user_agent='Posts lock threads to specified subreddit by /u/PeskyPotato')


# Subreddit to post to
SUB = 'test'
# Subs to blackslit, e.g. ['test', 'AskReddit']
BLACKLIST = []
# Sleep between searches
SLEEP = 300
# Max size of buffer
BUFFER_SIZE = 5000

# Buffer
buffer = []


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

'''
Checks each submission in the buffer if its not locked, not NSFW and not in blacklist, then calls 
postSub on the submssion.
'''
def checkBuffer():
    for sub_id in buffer:
        print("checking", sub_id, end="\r")
        submission = reddit.submission(id=sub_id)
        if submission.locked and (not submission.over_18) and str(submission.subreddit) not in BLACKLIST:
            postSub(submission)
            buffer.remove(str(submission.id))

'''
Posts submission to targetted subreddit if does not exist in the table
'''
def postSub(submission):
    link = "https://reddit.com"+submission.permalink
    if(dbWrite(submission.permalink, submission.title, submission.created, submission.author)):
        try:
            reddit.subreddit(SUB).submit(str(submission.title), url=link)
        except praw.exceptions.APIException:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "You are doing too much, trying to post again in 15 minutes")
            sleep(900)
            reddit.subreddit(SUB).submit(str(submission.title), url=link)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Posted",link)
        sleep(30)


'''
Gets posts from /r/all sorted by hot, if post is not locked, not NSFW and not on the blacklist 
then calls postSub on the submission.
'''
def populateBuffer():
    print("Populatebuffer")
    if len(buffer) > BUFFER_SIZE:
        del buffer[:(len(buffer)-BUFFER_SIZE)]
    print("Current buffer (after deletion):", len(buffer))
    for submission in reddit.subreddit('all').hot(limit=1000):
        if submission.locked and (not submission.over_18) and str(submission.subreddit) not in BLACKLIST:
            postSub(submission)
        elif str(submission.id) not in buffer:
            buffer.append(str(submission.id))


'''
Initialise bot
'''
if __name__ == '__main__':
    while(1):
        createTable()
        populateBuffer()
        print("Current buffer:", len(buffer))
        checkBuffer()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Sleeping for", SLEEP, "seconds.")
        sleep(SLEEP)
