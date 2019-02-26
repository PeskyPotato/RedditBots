'''
Collects top posts from the targeted subreddit SUB and makes
a post of the top 10 and stickies it while taking out 
lasts weeks post.
'''
import praw
import schedule
import time
import datetime


# API credentials, needs to have mod priviledges 
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='.',
                     user_agent='Sticky a submission filled with top posts of the week by /u/PeskyPotato')


# Targetted subreddit
SUB = 'techcrunch'

# Gets the date one week from today
one_week_timestamp = time.time() - (604800)
readable_date = datetime.datetime.fromtimestamp(one_week_timestamp).strftime('%d/%m/%y')
print(readable_date)

# Remove previous weeks sticky post
for submission in reddit.subreddit(SUB).hot(limit=5):
    if (submission.stickied and ': Newsletter' in submission.title):
        submission.mod.sticky(state=False)

# Gets the weeks top 10 posts and makes a submission and stickies it
def postSticky():
    title = '{}: Newsletter'.format(readable_date)
    body = 'Top posts of the week:\n\n'
    counter = 1
    for submission in reddit.subreddit(SUB).top('week', limit=10):
        body += '{}. [{}](https://www.reddit.com{})\n\n'.format(str(counter), submission.title, submission.permalink)
        counter += 1
    
    post = reddit.subreddit(SUB).submit(title, selftext=body)
    post.mod.sticky()

# postSticky()

# If you leave this file running 24/7 it will automatically post
# every Sunday and take down the old sticky. If you wish to run
# this manually on a weekly basis comment out everything below
# this and uncomment postSticky() above. Now every time you run 
# the file it will remove the old post and post a new newsletter.

schedule.every().monday.do(postSticky)

while True:
     schedule.run_pending()
     time.sleep(1)

