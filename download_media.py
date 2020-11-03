#encoding:utf8
from class_proxy import wrap
import json
import os
from progress.bar import IncrementalBar as Bar
import utils
import time
import asyncio
from aiohttp_requests import requests

def try_mkdir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError as error:
        print(error)

def collect_media_url(timeline):
    ret = {}
    for tweet in timeline:
        if tweet.entities.media:
            tweet_id = utils.gen_image_id(tweet)
            ret[tweet_id] = [media.media_url_https for media in tweet.entities.media]
    return ret

async def download_one_url(url, path, bar):
    r = await requests.get(url, timeout = 10)
    path = path + url[url.rfind("."):]
    if r.status != 200:
        print(f"Err getting:{url}")
        return False
    if os.path.exists(path): #if file exist, skip
        bar.next()
        return True
    content = await r.read()
    with open(path, "wb") as f:
        f.write(content)
    bar.next()
    return True

async def update_bar(bar):
    while True:
        await asyncio.sleep(1)
        bar.update()
        if bar.progress >= 1.0:
            bar.finish()
            break

async def download_media(id_urls):
    url_paths = {}
    for tweet_id, urls in id_urls.items():
        if len(urls) == 1:
            url = urls[0]
            path = os.path.join("images", tweet_id)
            url_paths[url] = path
            continue
        parent_path = os.path.join("images", tweet_id)
        try_mkdir(parent_path)
        for i, url in enumerate(urls, 1):
            path = os.path.join(parent_path, str(i))
            url_paths[url] = path
    urls = url_paths.keys()
    bar = Bar("Progress", max=len(urls), suffix="%(percent)d%% %(elapsed_td)s")
    tasks = [download_one_url(u, url_paths[u], bar) for u in urls]
    tasks.append(update_bar(bar))
    await asyncio.gather(*tasks)

def collect_and_download(timeline):
    id_urls = collect_media_url(timeline)
    try_mkdir("images")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_media(id_urls))

def standalone():
    timeline = []
    with open('timeline.json', 'r') as f:
        for line in f:
            tweet = json.loads(line)
            tweet = wrap(tweet)
            timeline.append(tweet)
    collect_and_download(timeline) 

if __name__ == "__main__":
    standalone()
