from Collection import Tokenizer, PreProcess, TwitterStream, pageCrawler
from Query import QueryGeneration, TRECProfile
from Relevance import simpleTitleMatch as tm
from kafka import KafkaConsumer, KafkaProducer
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
consumer.subscribe([topic])

dictlimit = dict.fromkeys(queryset.keys(), 10)
day = -1

# print (consumer.position)

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
         
        time = int(round(float(tweetjson['timestamp_ms'])/1000))
        newDay = datetime.datetime.fromtimestamp(time).day
        if newDay != day:
            day = newDay
            for topid in dictlimit:
                dictlimit[topid] = 10             
        for topid, query in queryset.items():
            query = queryset[topid]
            if tm.match(query, tweetjson):
                if dictlimit[topid] > 0:
                    print(topid, tweetjson['id'], time, runNo)
                    sys.stdout.flush()
                    dictlimit[topid]-=1
