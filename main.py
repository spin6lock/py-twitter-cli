#encoding:utf8
import twitter
import json
import config
from colorama import Fore, Style

api = twitter.Api(consumer_key=config.consumer_key,
        consumer_secret=config.consumer_secret,
        access_token_key=config.access_token_key,
        access_token_secret=config.access_token_secret)
timeline = api.GetHomeTimeline(count=config.count)
with open('timeline.json', 'w+') as f:
    for tweet in timeline:
        f.write(json.dumps(tweet._json))
        f.write('\n')
for tweet in timeline:
    print("-----------------")
    print(f"{Fore.YELLOW}@{tweet.user.screen_name}{Style.RESET_ALL}: {tweet.text} via: {Fore.BLUE}https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}{Style.RESET_ALL}")
