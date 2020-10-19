#encoding:utf8
import grequests
import twitter
import json
import config
import download_media
import display

api = twitter.Api(consumer_key=config.consumer_key,
        consumer_secret=config.consumer_secret,
        access_token_key=config.access_token_key,
        access_token_secret=config.access_token_secret)
timeline = api.GetHomeTimeline(count=config.count)
with open('timeline.json', 'w+') as f:
    for tweet in timeline:
        f.write(json.dumps(tweet._json))
        f.write('\n')

download_media.standalone()
display.standalone()
