import argparse
import logging
import configparser
import sys
from kafka import KafkaConsumer
import Query.QueryGeneration as QueryGeneration
import Query.TRECProfile as TRECProfile
import Relevance.api as RelMeasure
import Similarity.api as SimMeasure
import json
import datetime
from os import path
sys.path.append((path.dirname(path.dirname(path.abspath(__file__)))))
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
                    choices=set(('title', )),
                    help='indicating the method chosen for the relevance measurement.')
parser.add_argument('-T', '--relThreshold', default=0,
                    help='the threshold value for the relevance measurement method')
parser.add_argument('-d', '--similarity', required=True, default='jaccard',
                    choices=set(('None', 'jaccard', )),
                    help='indicating the method chosen for the similarity measurement.'
                         '"None" indicates not using similarity measurement.')
parser.add_argument('-U', '--simThreshold', default=0.6,
                    help='the threshold value for the similarity method')
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
            if RelMeasure.measure(tweet, query, args.relevance, args.relThreshold):
                if args.similarity == 'None':
                    logger_out.critical("{} {} {} {}".format(topic, tweet['id'], time, args.runname))
                    dictlimit[topic] -= 1
                    dict_submitted[topic].append(tweet)
                else:
                    if SimMeasure.measure(tweet, dict_submitted[topic], args.similarity, args.simThreshold):
                        logger_out.critical("{} {} {} {}".format(topic, tweet['id'], time, args.runname))
                        dictlimit[topic] -= 1
                        dict_submitted[topic].append(tweet)