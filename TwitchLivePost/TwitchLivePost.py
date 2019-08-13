'''
When run creates a submission for Twitch streamers that
are live.
'''
import requests
import praw
from datetime import datetime
from time import sleep

SUB = 'test'        # subreddit without /r/
TITLE_TEMPLATE = '%(user_name)s is currently streaming! - %(title)s'
SELFTEXT_TEMPLATE = ''

streamers = ['thebubbaarmy', 'spekel', 'uhsnow'] # add your list of twitch streamers (replace the current ones)
TWITCH_CLIENT = ''  #Twitch Client-ID

# Reddit API credentials
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='Posts live streamers from Twitch to Reddit by /u/PeskyPotato')


def date_print(message):
    '''Prints messages with date'''
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)


def make_submission():
    data = fetch_streams()
    for streamer in data['data']:
        date_print(streamer['user_name'] + ' is live')
        try:
            if SELFTEXT_TEMPLATE:
                reddit.subreddit(SUB).submit(TITLE_TEMPLATE % (streamer), selftext=SELFTEXT_TEMPLATE % (streamer))
            else:
                reddit.subreddit(SUB).submit(TITLE_TEMPLATE % (streamer), url='https://twitch.tv/%s' % (streamer['user_name']))
            sleep(60)
        except praw.exceptions.APIException as e:
            if 'RATELIMIT' in str(e):
                date_print(e)
                sleep(900)


def fetch_streams():
    '''Returns JSON of live streamers'''
    url = 'https://api.twitch.tv/helix/streams'
    q = '?'
    for streamer in streamers:
        if len(q) != 1:
            q += '&user_login='+streamer
        else:
            q += 'user_login='+streamer

    headers = {'Client-ID': TWITCH_CLIENT}
    r = requests.get(url + q, headers=headers)

    if r.status_code == 200:
        data = r.json()
        print(data)
    else:
        print("Invalid request", r.status_code)
        r.raise_for_status()

    return data


def main():
    make_submission()
    date_print('Complete')


main()
