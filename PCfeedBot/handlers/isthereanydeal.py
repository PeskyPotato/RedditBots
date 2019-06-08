import requests
import json
from difflib import SequenceMatcher

with open('config.json', 'r') as f:
    config_data = json.load(f)

def get_itad_url(title):
    url = "https://api.isthereanydeal.com/v01/search/search/?key={}&q={}&limit=20".format(config_data["isad_key"], title)
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        try:
            for game in data["data"]["list"]:
                if SequenceMatcher(None, title, game["title"]).ratio() > 0.7:
                    return game["urls"]["game"]
        except Exception as e:
            print(e)
        # if len(data["data"]["list"]) > 0:
        #     return data["data"]["list"][0]["urls"]["game"]
    else:
        print("Invalid request", r.status_code)

    return None



