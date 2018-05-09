import json

from kafka import KafkaConsumer

import Notebooks.consumer_config as config

topic = config.topic

consumer = KafkaConsumer(value_deserializer=lambda v: json.loads(v.decode('utf-8')))
consumer.subscribe([topic])

for message in consumer:
    tweet = message.value
    print (tweet)
    # process each tweet
