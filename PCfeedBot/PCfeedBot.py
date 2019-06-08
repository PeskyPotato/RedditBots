'''
Custom bot that goes throw game website to gather information
and posts it to /r/PCfeed as a comment.
'''
import praw
from time import sleep, strftime
from datetime import datetime
import sqlite3
import json
from handlers.steam import *
from handlers.isthereanydeal import * 
from handlers.igdb import *
from handlers.gog import *

with open('config.json', 'r') as f:
    config_data = json.load(f)

reddit = praw.Reddit(client_id=config_data["reddit_client_id"],
                     client_secret=config_data["reddit_client_secret"],
                     username=config_data["reddit_username"],
                     password=config_data["reddit_password"],
                     user_agent='Comments on info on /r/PCfeed by /u/PeskyPotato')


words_to_remove = config_data["words_to_remove"]

def checkSubmissions():
    for submission in reddit.subreddit(config_data["subreddit"]).top(limit=10):
        error = False
        error_message = "Submission title: {}\n\n url: {}\n\n".format(submission.title, submission.url)
        title = submission.title
        description = ""
        reply = "/r/PCfeed is a sub-Reddit dedicated to PC game releases and insightful commentary, without the marketing. For more information, please read the sidebar.\n\n"

        print("submission", title, submission.url)
        
        for word in words_to_remove:
            title = title.replace(word, "")
        
        url = submission.url

        if "https://store.steampowered.com/" in url:
            steam_data = get_steam_description(url)
            steam_title = steam_data[0]
            steam_description = steam_data[1]
            if steam_title and steam_description:
                title = steam_title
                description = steam_description
            else:
                print("Error\n Title:",title, "\n Description:", description)
                error_message += "Error Title: {} \n\n Description: {}\n\n".format(title, description)
                error = True
                

        # print("proper title", title, url)
        # print("description", description)

        #itad
        itad_url = get_itad_url(title)
        if itad_url:
            pass
            # print("itad", itad_url)
        else:
            # print("Error\n itad url", itad_url)
            error_message += "itad url: {}\n\n".format(itad_url)
            error = True
        
        #igdb
        igdb_url = get_igdb_url(title)
        if igdb_url:
            pass
            # print("igdb", igdb_url)
        else:
            # print("Error\n igdb url", igdb_url)
            error_message += "igdb url: {}".format(igdb_url)
            error = True
        #gog
        gog_url = get_gog_link(title)

        if error:
            print(error_message)
            reddit.subreddit(config_data["subreddit"]).message("Error: {}".format(submission.title), error_message)

        else:
            reply += "[IGDB]({}) - **{}** - {}\n\n [IsThereAnyDeal]({})\n\n".format(igdb_url, title, description, itad_url)
            if gog_url:
                reply += "[GOG]({})".format(gog_url)
            print(reply)
            submission.reply(reply)
        
        print("-------------\n\n")

def main():
    checkSubmissions()

main()
