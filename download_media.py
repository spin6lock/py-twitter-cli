#encoding:utf8
from class_proxy import wrap
import json
import grequests
import os
from progress.bar import IncrementalBar as Bar

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
            ret[tweet.id_str] = [media.media_url_https for media in tweet.entities.media]
    return ret

def download_one_url(r, path):
    url = r.url
    path = path + url[url.rfind("."):]
    if r.status_code != 200:
        print(f"Err getting:{url}")
        return False
    if os.path.exists(path): #不用重复下载了
        return True
    with open(path, "wb") as f:
        f.write(r.content)
    return True

def download_media(id_urls):
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
    rs = (grequests.get(u, stream=False, timeout = 10) for u in urls)
    for resp in grequests.imap(rs, size = 10):
        bar.next()
        if resp:
            download_one_url(resp, url_paths[resp.url])
        else:
            print("download error")
    bar.finish()

def collect_and_download(timeline):
    id_urls = collect_media_url(timeline)
    try_mkdir("images")
    download_media(id_urls)

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

