'''
Posts an image (in this case a nut) on the targeted subreddit (SUB)
with the last title + link in nuts.txt every day at the set time (TIME).
Each new post to be made my be placed on a new line with double colons,
"::", separating them, it will not work without them.
'''
import praw
import schedule
from time import sleep, strftime
from datetime import datetime

# API credentials, needs to have mod priviledges 
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='Posts images of nuts because why not? by /u/PeskyPotato')

# Time to run daily
TIME = '23:29'
SUB = 'test'

def submitNut():
    nut = getNut()
    if isinstance(nut, tuple):
        try:
            reddit.subreddit(SUB).submit(nut[0], url=nut[1])
        except praw.exceptions.APIException:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Rate limited, sleeping for 15 minutes")
            sleep(900)
            reddit.subreddit(SUB).submit(nut[0], url=nut[1])
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Posted", nut[0], nut[1])
    elif nut == 1:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "There are no nuts left :(")

def getNut():
    with open('nuts.txt', 'r') as f:
        nuts = f.read().splitlines()
    
    if len(nuts):
        nutOTD = nuts[-1]
        try:
            title = nutOTD.split("::")[0].strip()
            url = nutOTD.split("::")[1].strip()
            print(title, url)
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Incorrect nut.txt format")
            return None
        with open('nuts.txt', 'w') as f:
            for nut in nuts[:-1]:
                f.write(nut + '\n')

        if len(nuts) == 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Last nut has been used, refill your nuts for tomorrow.")
        return (title, url)
    return 1

schedule.every().day.at(TIME).do(submitNut)
while True:
    schedule.run_pending()
    sleep(1)
