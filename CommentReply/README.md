#Comment Reply 
> Replies to comments based on keywords with predfined responses

##Setup and Install

Read [this comprehensive guide](https://www.reddit.com/r/RequestABot/comments/3d3iss/a_comprehensive_guide_to_running_your_bot_that/) on getting a bot setup and running from /r/RequestABot. This bot was made using Python3 and uses Praw.

Download the `CommentReplyBot.py` and the `responses.txt` files.

The reddit `client_id`, `client_secret`, `username` and `password` go in the `CommentReplyBot.py` file along with the desired subreddit and keywords to listen for. The replies to be made go into the `responses.txt` file with each one on a new line. A random response will be selected when a keyword is spotted in the comments.

When you run the bot a `posted.db` file will be created, this file stores the ids of all the comments that the bot has replied to. In order for the bot not to reply to the same comment twice do not delete this file.