import requests
import json
from difflib import SequenceMatcher

with open('config.json', 'r') as f:
    config_data = json.load(f)

def get_igdb_url(title):
    title = title
    url = "https://api-v3.igdb.com/games/"
    headers = {"user-key":config_data["igdb_user_key"]}
    body = 'search "{}"; fields url, name;'.format(title)
    try:
        r = requests.post(url, data=body, headers=headers)
    except UnicodeEncodeError:
        # find a solution for this https://www.reddit.com/r/PCfeed/comments/bxwaqo/octopath_traveler/
        return None
    if r.status_code == 200:
        data = r.json()
        for game in data:
            if SequenceMatcher(None, title, game["name"]).ratio() > 0.7:
                return game["url"]
    else:
        print("Invalid request", r.status_code)

    return None

# print(get_igdb_url("Observation"))
