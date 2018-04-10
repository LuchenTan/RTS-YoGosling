from Collection import Tokenizer, PreProcess
from Query import QueryGeneration, TRECProfile
from Relevance import simpleTitleMatch as tm
from kafka import KafkaConsumer, TopicPartition
import json
from config import consumer_config as config
import datetime
import sys
from sklearn.metrics import jaccard_similarity_score

'''Consumes from kafka twitter api topic, does preprocessing, 
and output file with format topic_id, tweet_id, timestamp, run_no'''

"""
Add in Jaccard similarity from integration test run.
"""
runNo = "run1"

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
# submitted tweets
dict_submitted = dict.fromkeys(queryset.keys(), [])
jaccard_threshold = 0.6


for message in consumer:
    tweet = message.value
    # process each tweet
    tweetjson = prePro.process(tweet)
    if tweetjson:
        #print(tweetjson)
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
                    tweet_words = tweetjson['normal_words']
                    dup = False
                    for sub_json in dict_submitted[topid]:
                        if jaccard_similarity_score(sub_json['normal_words'], tweet_words) > jaccard_threshold:
                            dup = True
                            break
                    if not dup:
                        print(topid, tweetjson['id'], time, runNo)
                        sys.stdout.flush()
                        dictlimit[topid]-=1
                        dict_submitted[topid].append(tweetjson)
