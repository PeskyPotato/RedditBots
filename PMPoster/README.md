#PM Poster 
> Sends private messages to a user at a set time everyday.

##Setup and Install

Read [this comprehensive guide](https://www.reddit.com/r/RequestABot/comments/3d3iss/a_comprehensive_guide_to_running_your_bot_that/) on getting a bot setup and running from /r/RequestABot. This bot was made using Python3 and uses Praw.

Download the `PMPoster.py` and the `pms.txt` files.

The reddit `client_id`, `client_secret`, `username` and `password` go in the `PMPoster.py` file along with the desired reddit user and time to send. The replies to be made go into the `pms.txt` file. Each new message is to be placed on a new line with double colons, "::", separating the subject and body.
