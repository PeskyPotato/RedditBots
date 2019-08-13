# Twitch Live Post
> Replies to comments based on keywords with predfined responses

## Setup and Install
Read [this comprehensive guide](https://www.reddit.com/r/RequestABot/comments/3d3iss/a_comprehensive_guide_to_running_your_bot_that/) on getting a bot setup and running from /r/RequestABot. This bot was made using Python3 and uses Praw.

Download the `TwitchLivePost.py` file.

The reddit `client_id`, `client_secret`, `username` and `password` go in the `TwitchLivePost.py` file along with the desired subreddit and streamers to check for. Next get your Twitch API credentials from [their developer site](https://dev.twitch.tv/). Place the Client-ID in the `TwitchLivePost.py` file. 

Whenever you run this python script it will check for streamers specified in the list and submit a post in the specified subreddit if they are live. You can schedule this script to run at set times.
