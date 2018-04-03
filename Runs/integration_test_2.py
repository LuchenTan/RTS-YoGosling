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

# Load Profiles
rts16_path = "profiles/TREC2016-RTS-topics.json"
rts17_path = "profiles/RTS17-topics.json"
profile = TRECProfile.TRECProfileReader(rts17_path, 17)
profile.read()
queryset = dict()
for topid, topic in profile.topics.items():
    queryset[topid] = QueryGeneration.QueryGeneration(topic).getQuery()

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
dictlimit = dict.fromkeys(queryset.keys(), 10)
day = -1

tweet_url_titles = {}
with open("sample_url_titles.txt") as f:
    lines = f.readlines()
    for line in lines:
        tweetJson = json.loads(line)
        tweet_url_titles[tweetJson["id"]] = tweetJson["titles"]

for message in consumer:
    tweet = message.value
    # process each tweet
    tweetjson = prePro.process(tweet)
    if tweetjson:
        # print(tweetjson['normal_words'])
        time = int(round(float(tweetjson['timestamp_ms'])/1000))
        newDay = datetime.datetime.fromtimestamp(time).day
        if newDay != day:
            day = newDay
            for topid in dictlimit:
                dictlimit[topid] = 10             
        for topid, query in queryset.items():
            query = queryset[topid]
            result = False
            if topic in tweet_url_titles:
                result = tm.match_titles(query, tweet_url_titles[topic]) 
            if result or tm.match(query, tweetjson):
                if dictlimit[topid] > 0:
                    print(topid, tweetjson['id'], time, runNo)
                    sys.stdout.flush()
                    dictlimit[topid]-=1
