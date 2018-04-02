from Collection import Tokenizer, PreProcess, pageCrawler
from Query import QueryGeneration, TRECProfile
from Relevance import simpleTitleMatch as tm
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
import json
from config import consumer_config as config
import datetime
import sys

'''Consumes from kafka twitter api topic, does preprocessing, and output file with format topic_id, tweet_id, timestamp, run_no'''

runNo = "run0"

if len(sys.argv) > 1:
    runNo = sys.argv[1]

# Load tweets
topic = config.topic

tknzr = Tokenizer.MyTweetTokenizer()
prePro = PreProcess.PreProcessor(tknzr.tokenize)

consumer = KafkaConsumer(value_deserializer=lambda v: json.loads(v.decode('utf-8')))

partition = TopicPartition(topic, 0)
consumer.assign([partition])


offset = 0

with open("last_offset.txt") as f:
    offset = int(f.read())

consumer.seek(partition, offset)

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         batch_size=50000)
topic = 'tweet_url_titles'

for message in consumer:
    tweet = message.value
    # process each tweet
    tweetjson = prePro.process(tweet)
    if tweetjson:
        urls = tweetjson['urls']
        titles = pageCrawler.pageCrawler(urls)
        if len(titles) > 0:
            producer.send(topic, {'id': tweetjson['id'], 'titles':titles}) 
