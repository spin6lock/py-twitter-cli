#encoding:utf8
import json
from class_proxy import wrap
import os
import config
import utils

def display_one_tweet_image(tweet, fout):
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
    fout.write('<img src={} style="height:{}">'.format(path, config.image_height))

def display(timeline):
    filename = 'timeline.html'
    with open(filename, "w") as fout:
        fout.write("<table border='1'>")
        for tweet in timeline:
            fout.write("<tr><td>")
            link = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"
            fout.write(f'<a href="https://twitter.com/{tweet.user.screen_name}">@{tweet.user.screen_name}</a>: {tweet.text} via: <a href="{link}">{link}</a>')
            if tweet.entities.media:
                display_one_tweet_image(tweet, fout)
            fout.write("</tr></td>")
        fout.write("</table>")


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
