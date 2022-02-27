#encoding:utf8
import json
from class_proxy import wrap
import os
import config
import utils
import subprocess
import re

def display_one_tweet_image(tweet, fout):
    path = None
    if utils.is_contains_multiple_media(tweet):
        medias = tweet.extended_entities.media
        tweet_id = utils.gen_image_id(tweet)
        parent_path = os.path.join("images", tweet_id)
        for i, media in enumerate(medias, 1):
            url = media.media_url_https
            postfix = url[url.rfind("."):]
            path = os.path.join(parent_path, str(i) + postfix)
            fout.write('<img src={} style="height:{}">'.format(path, config.image_height))
    else:
        media = tweet.entities.media[0]
        url = media.media_url_https
        postfix = url[url.rfind("."):]
        image_id = utils.gen_image_id(tweet)
        path = os.path.join("images", image_id+postfix)
        fout.write('<a href={}><img src={} style="height:{}"></a>'.format(path, path, config.image_height))


pattern = re.compile("https:\/\/t\.co\/[a-zA-Z0-9]+")
def add_link_for_text(tweet):
    # media url, don't add link
    if tweet.entities.media:
        return tweet.text or ''
    else:
        text = tweet.full_text
        if tweet.retweeted_status:
            text = tweet.retweeted_status.full_text
        urls = pattern.findall(str(text))
        if len(urls) > 0:
            text = text.replace(urls[0], '')
            for url in urls[1:]:
                text = text.replace(url, f'<a href="{url}">{url}</a>')
        return text


def display(timeline):
    filename = 'timeline.html'
    with open(filename, "w") as fout:
        fout.write("<table border='1' style='width:800px;table-layout:fixed;'>")
        for tweet in timeline:
            fout.write("<tr><td>")
            link = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"
            text = add_link_for_text(tweet)
            fout.write(f'<a href="https://twitter.com/{tweet.user.screen_name}">@{tweet.user.screen_name}</a>: {text} <a href="{link}">source</a>')
            if tweet.entities.media:
                display_one_tweet_image(tweet, fout)
            fout.write("</tr></td>")
        fout.write("</table>")
    subprocess.call(["firefox", "timeline.html"])


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
