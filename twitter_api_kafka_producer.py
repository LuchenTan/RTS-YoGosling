from twython import TwythonStreamer
from kafka import KafkaProducer
import json
import sys
import config.producer_api_config as config

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        producer.send(topic, data)

    def on_error(self, status_code, data):
        print(status_code)

topic = config.topic
keyword = config.keyword
batchsize = config.batchsize
oauth = config.oauth

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), batch_size=batchsize)
stream = MyStreamer(**oauth)

if keyword == 'all':
    stream.statuses.sample()
else:
    stream.statuses.filter(track=keyword)
