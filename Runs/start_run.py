import argparse
import logging
import configparser
import sys
from os import path
sys.path.append((path.dirname(path.dirname(path.abspath(__file__)))))
from kafka import KafkaConsumer
import Query.QueryGeneration as QueryGeneration
import Query.TRECProfile as TRECProfile
import Relevance.api as RelMeasure
import Similarity.api as SimMeasure
import json
import datetime


run_config_path = path.join(path.dirname(__file__), '../config/runs.ini')
producer_config_path = path.join(path.dirname(__file__), '../config/producer.ini')


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', choices=set(('stream', 'archive')),
                    help='indicating input source using term "stream" or "archive". '
                         'stream for listening Twitter Streaming API;'
                         'archive for reading from files on disk.',
                    required=True)

url_parser = parser.add_mutually_exclusive_group(required=False)
url_parser.add_argument('--crawl-url', dest='url', action='store_true',
                        help='indicating crawling the titles of web links in each tweet')
url_parser.add_argument('--no-crawl-url', dest='url', action='store_false',
                        help='indicating not crawling the web link titles')
parser.set_defaults(url=False)

parser.add_argument('-o', '--output', required=True, default='rts-runA.txt',
                    help='location for storing output results')
parser.add_argument('-r', '--runname', required=True, default='runA',
                    help='indicating the name of this run.')
parser.add_argument('-m', '--relevance', required=True, default='title',
                    choices=set(('title', 'simpleCount', )),
                    help='indicating the method chosen for the relevance measurement.')
parser.add_argument('-T', '--relThreshold', default=0.1,
                    help='the threshold value for the relevance measurement method', type=float)
parser.add_argument('-d', '--similarity', required=True, default='jaccard',
                    choices=set(('None', 'jaccard', )),
                    help='indicating the method chosen for the similarity measurement.'
                         '"None" indicates not using similarity measurement.')
parser.add_argument('-U', '--simThreshold', default=0.6,
                    help='the threshold value for the similarity method', type=float)
parser.add_argument('-w', '--window', default=0, type=int,
                    help='indicating the length of a pushing window (in seconds). '
                         'Default value is 0 -- push immediately.')
args = parser.parse_args()


# logging.basicConfig(
#     format='%(message)s',
#     handlers=[
#         logging.FileHandler(args.output),
#         logging.StreamHandler()
#     ],
#     filemode='w',
#     level=logging.INFO
# )
logging.basicConfig(format='%(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

logger_out = logging.getLogger('out')
logger_out.addHandler(logging.FileHandler(args.output, mode='w'))
logger_out.setLevel(logging.CRITICAL)

config = configparser.ConfigParser()
config.read(run_config_path)

producer_config = configparser.ConfigParser()
producer_config.read(producer_config_path)

if args.source == 'archive':
    section = 'ARCHIVE'
elif args.source == 'stream':
    section = 'STREAM'
else:
    section = 'STREAM'  # default

if args.url:
    topic = producer_config[section]['processed_topic_crawled']
else:
    topic = producer_config[section]['processed_topic_nocrawl']

consumer = KafkaConsumer(topic,
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest', enable_auto_commit=True,
                         consumer_timeout_ms=600000)  # close consumer if no response for 10mins

profile = TRECProfile.TRECProfileReader(config['PROFILE']['location'], config['PROFILE']['year'])
profile.read()
queryset = dict()
for topid, topic in profile.topics.items():
    queryset[topid] = QueryGeneration.QueryGeneration(topic).getQuery()

dictlimit = dict.fromkeys(queryset.keys(), int(config['SYSTEM']['volumn']))
day = -1
# submitted tweets
dict_submitted = dict.fromkeys(queryset.keys(), [])
max_score_tweet = dict.fromkeys(queryset.keys(), {'tweet': {}, 'score': args.relThreshold})

windowSize = args.window
lastPush = dict.fromkeys(queryset.keys(), int(int(producer_config['ARCHIVE']['startpoint'])/float(1000)))
for message in consumer:
    tweet = message.value
    time = int(round(float(tweet['timestamp_ms'])/1000))
    newDay = datetime.datetime.fromtimestamp(time).day
    if newDay != day:
        day = newDay
        for topic in dictlimit:
            dictlimit[topic] = int(config['SYSTEM']['volumn'])
    for topic, query in queryset.items():
        if dictlimit[topic] > 0:
            # select the push
            score = float(RelMeasure.measure(tweet, query, args.relevance, args.relThreshold))
            if score >= max_score_tweet[topic]['score']:
            #if (time - lastPush) >= windowSize:
                if args.similarity == 'None':
                    simMeasure = True
                else:
                    simMeasure = SimMeasure.measure(tweet, dict_submitted[topic], args.similarity, args.simThreshold)
                if simMeasure:
                    max_score_tweet[topic] = {'tweet': tweet, 'score': score}
                    if (time - lastPush[topic]) >= windowSize:
                        logger_out.critical("{} {} {} {}".format(topic, max_score_tweet[topic]['tweet']['id'], time, args.runname))
                        dictlimit[topic] -= 1
                        dict_submitted[topic] = dict_submitted[topic] + [max_score_tweet[topic]['tweet']]
                        # print([(topic, item) for topic, item in dict_submitted.items() if len(item) > 0])
                        lastPush[topic] = time
                        max_score_tweet[topic] = {'tweet': {}, 'score': args.relThreshold}
                        # print([(topic, item) for topic, item in max_score_tweet.items() if item['score'] > args.relThreshold])

