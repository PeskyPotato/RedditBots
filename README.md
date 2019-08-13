# RedditBots

I have decided to make this repository for all the little Reddit bots I have written over the years instead of sharing them via gists or Pastebin. This would make it easier to maintain and keep all the scripts organised.

## FlairCrossposter
Crossposts a submission with a specific flair to a targeted subreddit. The post is saved in a database and checked to make sure the submission is not already crossposted by the bot.

## ImagePoster
Posts a picture of a nut with a user defined title daily at a set time.

## LockedCrosspost
If a post is locked this bot posts to the specified subreddit.

## Newsletter
Collects top posts from the targeted subreddit SUB and makes a post of the top 10 and stickies it while taking out lasts weeks stickied submission.

## NewUsers
Adds new users of a subreddit to a database and prints them out. This gets usernames from submissions as well as comments and replies.

## PMPoster
Send a daily private message to a specified redditor based on a set time and a list of messages

## TwitchLivePost
Replies to comments based on keywords with predfined responses

## TwitterPost
Checks submissions on a given subreddit over a fixed interval, if
the submission url is a tweet, the tweet text and images are
entered into a comment.

## TwitterSubPoster
Grabs submission from a given subreddit over a fixed interval and tweets the
set amount of posts. The tweets are recorded in a database to prevent
tweeting duplicate posts. A delay is added to avoid spamming twitter.

## WordOfTheDay
Posts a selftext on the targeted subreddit with a word every day at a set time.

## Other
These are scripts in other repositories that I've worked with or created

- [RedditImageBackup](https://github.com/LameLemon/RedditImageBackup) - Downloads images, gifs and text posts from Reddit and sorts them into folders
