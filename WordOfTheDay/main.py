'''
Posts a selftext on the targeted subreddit (SUB) with the last word 
in words.txt every day at a set time (TIME).
'''

import praw
import random
import datetime
import schedule
import time

reddit = praw.Reddit(username = '', password = '',
                    client_id = '', client_secret= '',
                    user_agent= 'Post Word of the day /u/PeskyPotato')

TIME = '12:44' # Replace with time to run daily
SUB = 'calligraffiti' 

def submitWord():
    word = getWord()
    if word:
        title = "WotD " + datetime.datetime.today().strftime('%d/%m/%y') + " - " + word
        reddit.subreddit(SUB).submit(title, selftext='Post pictures of your work here!')
        print("Posted WoTD", word)
    else:
        print("There are no words left")

def getWord():
    with open('words.txt', 'r') as f:
        words = f.read().splitlines()

    
    if len(words):
        wordOTD = words[-1]
        with open('words.txt', 'w') as f:
            for word in words[:-1]:
                f.write(word + '\n')
        
        if len(words) == 1:
            print("Last word has been used, make sure to add more for tomorrow")
        return wordOTD


schedule.every().day.at(TIME).do(submitWord)

while True:
    schedule.run_pending()


