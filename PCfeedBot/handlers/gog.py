import json
import requests
from difflib import SequenceMatcher


def get_gog_link(title):
    r = requests.get("https://www.gog.com/games/ajax/filtered?limit=20&search={}".format(title.replace(" ", "+")))

    if r.status_code == 200:
        data = r.json()
        for product in data["products"]:
            if SequenceMatcher(None, title, product["title"]).ratio() > 0.7:
                return "https://www.gog.com"+product["url"]
    else:
        print("Invalid request", r.status_code)

    return None

# print(get_gog_link("Production Line"))