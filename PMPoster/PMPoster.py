'''
Send a private message to a specified redditor (USER) with a subject 
and message body every day at the set time (TIME). Each new message is 
to be placed on a new line with double colons, "::", separating the 
subject and body.
'''

import praw
import schedule
import sys
from time import sleep, strftime
from datetime import datetime

# Reddit API credentials
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='Sends pms to a single user by /u/PeskyPotato')

# Time to run daily
TIME = '18:29'
USER = 'testuser'

def sendPM():
    pm = getPM()
    if isinstance(pm, tuple):
        try:
            reddit.redditor(USER).message(pm[0], pm[1].encode('utf-8').decode('unicode_escape'))
        except praw.exceptions.APIException as e:
            print(e)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Rate limited, sleeping for 15 minutes")
            sleep(900)
            reddit.redditor(USER).message(pm[0], pm[1])
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Sent", pm[0], pm[1])
    elif pm == 1:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "There are no pms left.")

def getPM():
    try:
        with open('pms.txt', 'r') as f:
            pms = f.read().splitlines()
    except FileNotFoundError as e:
        print('"pms.txt" does not exist, please create the file and use the correct format.')
        sys.exit()

    if len(pms):
        pmOTD = pms[-1]
        try:
            subject = pmOTD.split("::")[0].strip()
            body = pmOTD.split("::")[1].strip()
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Incorrect pms.txt format")
            return None
        with open('pms.txt', 'w') as f:
            for pm in pms[:-1]:
                f.write(pm + '\n')

        if len(pms) == 1:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Last PM has been used, refill your PMs for tomorrow.")
        elif len(pms) == 2:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "One PM left, remember to refill your PMs.")
        return (subject, body)

    return 1

schedule.every().day.at(TIME).do(sendPM)
while True:
    schedule.run_pending()
    sleep(1)
