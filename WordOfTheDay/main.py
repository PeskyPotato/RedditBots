'''
Posts a selftext on the targeted subreddit (SUB) with the last word 
in words.txt every day at the set time (TIME). Place each new word
on a new line.
'''

import praw
import random
import datetime
import schedule
from time import sleep, strftime
from datetime import datetime

reddit = praw.Reddit(username = '', password = '',
                    client_id = '', client_secret= '',
                    user_agent= 'Post Word of the day /u/PeskyPotato')

# Time to run daily
TIME = '12:44'
SUB = 'calligraffiti' 

def submitWord():
    word = getWord()
    if word:
        title = "WotD " + datetime.datetime.today().strftime('%d/%m/%y') + " - " + word
        try: 
            reddit.subreddit(SUB).submit(title, selftext='Post pictures of your work here!')
        except praw.exceptions.APIException:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Rate limited, sleeping for 15 minutes")
            sleep(900)
            reddit.subreddit(SUB).submit(title, selftext='Post pictures of your work here!')

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Posted WoTD", word)
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "There are no words left")

def getWord():
    with open('words.txt', 'r') as f:
        words = f.read().splitlines()

    
    if len(words):
        wordOTD = words[-1]
        with open('words.txt', 'w') as f:
            for word in words[:-1]:
                f.write(word + '\n')
        
        if len(words) == 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Last word has been used, make sure to add more for tomorrow")
        return wordOTD


schedule.every().day.at(TIME).do(submitWord)

while True:
    schedule.run_pending()
    sleep(1)


