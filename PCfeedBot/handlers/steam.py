from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request

def get_steam_description(url):
    req = Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
    )

    uClient = urlopen(req)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "lxml")
    try:
        title = page_soup.find_all("div", {"class": "apphub_AppName"})[0].text
        description = page_soup.find_all("div", {"class": "game_description_snippet"})[0].text.strip()
        return (title, description)
    except Exception as e:
        print(e)
        return None
    
# get_steam_description("https://store.steampowered.com/app/370870/Dark_Future_Blood_Red_States/")
