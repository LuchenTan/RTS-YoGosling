from Collection import Tokenizer, PreProcess, pageCrawler
from Query import QueryGeneration, TRECProfile
from Relevance import simpleTitleMatch as tm
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
import json
from config import consumer_config as config
import datetime
import sys

if len(sys.argv) > 1:
    runNo = sys.argv[1]

# Load tweets
tweetsTopic = config.topic

consumerTweets = KafkaConsumer(value_deserializer=lambda v: json.loads(v.decode('utf-8')))

tweetsPartition = TopicPartition(tweetsTopic, 0)
consumerTweets.assign([tweetsPartition])

offsetTweets = 0
with open("last_offset.txt") as f:
    offsetTweets = int(f.read())

consumerTweets.seek(tweetsPartition, offsetTweets)

# titles
titlesTopic = config.titlesTopic
consumerTitles = KafkaConsumer(value_deserializer=lambda v: json.loads(v.decode('utf-8')))

titlesPartition = TopicPartition(titlesTopic, 0)
consumerTitles.assign([titlesPartition])

offsetTitles = 0
with open("last_offset_titles.txt") as f:
    offsetTitles = int(f.read())

consumerTitles.seek(titlesPartition, offsetTitles)

tknzr = Tokenizer.MyTweetTokenizer()
prePro = PreProcess.PreProcessor(tknzr.tokenize)

# producer
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         batch_size=50000)

for message in consumerTitles:
    tweetTitles = message.value
    # print (tweetTitles)
    tweetTitleId = tweetTitles['id']
    titles = tweetTitles['titles']
    if titles:
       while True:
           tweets = consumerTweets.poll(timeout_ms=1000, max_records=1)[tweetsPartition][0].value
           tweetId = tweets['id']
           tweetjson = prePro.process(tweets)
           if tweetjson:
               if tweetId == tweetTitleId:
                   tweetjson['crawled_pages'] = titles
               else:
                   tweetjson['crawled_pages'] = []
               producer.send("tweets_merged", tweetjson)
           if tweetId == tweetTitleId:
               break
