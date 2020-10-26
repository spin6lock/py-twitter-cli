#encoding:utf8
from colorama import Fore, Style
import json
from class_proxy import wrap
from imgcat import imgcat
import os
import config
import utils

def display_one_tweet_image(tweet):
    path = None
    if len(tweet.entities.media) > 1:
        parent_path = os.path.join("images", tweet.id_str)
        for i, media in enumerate(tweet.entities.media, 1):
            url = media.media_url_https
            postfix = url[url.rfind("."):]
            path = os.path.join(parent_path, str(i) + postfix)
    else:
        media = tweet.entities.media[0]
        url = media.media_url_https
        postfix = url[url.rfind("."):]
        image_id = utils.gen_image_id(tweet)
        path = os.path.join("images", image_id+postfix)
    try:
        with open(path, "rb") as f:
            imgcat(f.read(), height = config.image_height)
    except FileNotFoundError as err:
        print(err)

def display(timeline):
    for tweet in timeline:
        print("-----------------")
        print(f"{Fore.YELLOW}@{tweet.user.screen_name}{Style.RESET_ALL}: {tweet.text} via: {Fore.BLUE}https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}{Style.RESET_ALL}")
        if tweet.entities.media:
            display_one_tweet_image(tweet)

def standalone():
    timeline = []
    with open('timeline.json', 'r') as f:
        for line in f:
            tweet = json.loads(line)
            tweet = wrap(tweet)
            timeline.append(tweet)
    display(timeline)

if __name__ == "__main__":
    standalone()
