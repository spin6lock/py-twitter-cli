#encoding:utf8
import twitter
import json
import config
import download_media
import gen_webpage
import class_proxy

api = twitter.Api(consumer_key=config.consumer_key,
        consumer_secret=config.consumer_secret,
        access_token_key=config.access_token_key,
        access_token_secret=config.access_token_secret)
timeline = api.GetHomeTimeline(count=config.count)
new_timeline = []
with open('timeline.json', 'w+') as f:
    for tweet in timeline:
        new_timeline.append(class_proxy.wrap(tweet._json))
        f.write(json.dumps(tweet._json))
        f.write('\n')

download_media.collect_and_download(new_timeline)
gen_webpage.display(new_timeline)
