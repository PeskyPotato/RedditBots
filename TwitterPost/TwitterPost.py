'''
Checks submissions on a given subreddit over a fixed interval, if
the submission url is a tweet, the tweet text and images are
entered into a comment.
'''
import tweepy
from tweepy import OAuthHandler
import praw

# Reddit credentials go below
reddit = praw.Reddit(client_id = '',
                     client_secret= '',
                     user_agent= '',
                     username = '',
                     password = '')

# Twitter credentials go below
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

def grabber(subR):
    for submission in reddit.subreddit(subR).new(limit=100):
        link = submission.url
        if 'https://twitter.com/'  in link and '/status/' in link:
            print(link)
            tweet_id = link[-18:]

            tweet_info = grab_tweet(tweet_id)

            # Checks for images
            if 'media' in tweet_info.entities:
                for image in tweet_info.entities['media']:
                    media = image['media_url']
                submission.reply('[@{}](https://www.twitter.com/{})\n \n >[{}]({}) \n \n >{} \n \n [Attached image]({})'
                .format(tweet_info.user.screen_name,
                tweet_info.user.screen_name,
                tweet_info.created_at,
                link, tweet_info.full_text,
                media))
            else:
                submission.reply('[@{}](https://www.twitter.com/{})\n \n >[{}]({}) \n \n >{}'
                .format(tweet_info.user.screen_name,
                tweet_info.user.screen_name,
                tweet_info.created_at,
                link, tweet_info.full_text))


def grab_tweet(tweet_id):
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    return tweet

if __name__ == '__main__':
    # Subreddit to comment on goes below
    # An infinite loop with a time delay can be set up too
    grabber('test')
