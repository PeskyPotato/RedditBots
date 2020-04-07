#!/usr/bin/env python3
'''
Sends a message to a discord channel through a webhook
when a new message is posted to a subreddit. Add or edit 
a subreddit by adding a new black to subs.json.
'''
import requests
import json
from datetime import datetime

headers = {"User-Agent": "reddit-new-post-notifier"}

DISCORD_WEBHOOK = ""

def new_post(submission):
    print(datetime.now().strftime("%Y-%m-%d %H:%M"), submission["title"], submission["ups"], submission["downs"])
    print("https://reddit.com"+submission["permalink"])
    print("-----")

    payload = {
        "username": "Hibiki",
        "avatar_url": "https://i.imgur.com/IFPMBBC.jpg",
        "content": 'https://reddit.com/' + submission['permalink'],
    }

    r = requests.post(DISCORD_WEBHOOK, data = payload)

def check_subs(sub_data):
    sub = sub_data["subreddit"]
    last_utc = sub_data["last_utc"]
    url = "http://www.reddit.com/r/"+sub+"/new.json?sort=new&limit=10"

    res = requests.get(url, headers = headers)
    if res.status_code == requests.codes.ok:
        data = res.json()
        current_utc = 0
        for submission in data["data"]["children"][:1]:
            if submission["data"]["created_utc"] > last_utc:
                new_post(submission["data"])
                if submission["data"]["created_utc"] > current_utc:
                    current_utc = submission["data"]["created_utc"]
        if current_utc != 0:
            last_utc = current_utc
    return last_utc

def main():
    json_file = "./subs.json"
    
    with open(json_file) as f:
        subs = json.load(f)
    
    index = 0
    for sub in subs:
        subs[index]["last_utc"] = check_subs(sub)
        index += 1

    with open(json_file, "w") as f:
        json.dump(subs, f)
    

if __name__ == "__main__":
    main()
 