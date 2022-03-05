#encoding:utf8
import json
from class_proxy import wrap
import os
import config
import utils
import subprocess
import re


img_style = f"height:{config.image_height}"
def img_gen(src, style=img_style):
    return f'<img src={src} style="{style}" >'


def ahref_gen(text, link):
    return f"<a href='{link}' target='_blank'>{text}</a>"


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
            fout.write(img_gen(path))
    else:
        media = tweet.entities.media[0]
        url = media.media_url_https
        postfix = url[url.rfind("."):]
        image_id = utils.gen_image_id(tweet)
        path = os.path.join("images", image_id+postfix)
        image_tag = img_gen(path)
        fout.write(ahref_gen(image_tag, path))


def get_text_from(tweet):
    text = tweet.full_text
    if tweet.quoted_status:
        text = f"{text} Quote: {tweet.quoted_status.full_text}"
    if tweet.retweeted_status:
        ret_text = get_text_from(tweet.retweeted_status)
        text = f"{text} RT: {ret_text}"
    return text


pattern = re.compile("https:\/\/t\.co\/[a-zA-Z0-9]+")
def add_link_for_text(tweet):
    text = get_text_from(tweet)
    urls = pattern.findall(str(text))
    if len(urls) > 0:
        text = text.replace(urls[0], '')
        for url in set(urls[1:]):
            url_link = ahref_gen(url, url)
            text = text.replace(url, url_link)
    return text


def display(timeline):
    filename = 'timeline.html'
    with open(filename, "w") as fout:
        fout.write("<table border='1' style='width:800px;table-layout:fixed;'>")
        for tweet in timeline:
            fout.write("<tr><td>")
            link = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"
            text = add_link_for_text(tweet)
            name_link = f"https://twitter.com/{tweet.user.screen_name}"
            tweet_head = ahref_gen(f"@{tweet.user.screen_name}", name_link)
            source = ahref_gen("source", link)
            fout.write(f'{tweet_head}: {text} {source}')
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
