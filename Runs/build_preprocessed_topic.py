import argparse
import configparser
import json
import logging
import sys
from os import path

from kafka import KafkaConsumer, KafkaProducer

import Collection.pageCrawler as pageCrawler
import Collection.PreProcess as PreProcess
import Collection.Tokenizer as Tokenizer

sys.path.append((path.dirname(path.dirname(path.abspath(__file__)))))
config_path = path.join(path.dirname(__file__), '../config/producer.ini')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# read configuration file
config = configparser.ConfigParser()
config.read(config_path)


# setup arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', choices=set(('stream', 'archive')),
                    help='indicating input source using term "stream" or "archive". '
                         'stream for listening Twitter Streaming API;'
                         'archive for reading from files on disk.',
                    required=True)
parser.add_argument('-u', '--url', type=bool, default=True,
                    help='whether want to crawl the titles of urls in each tweet')

args = parser.parse_args()


if args.source == 'archive':
    section = 'ARCHIVE'
elif args.source == 'stream':
    section = 'STREAM'
else:
    section = 'STREAM'  # default

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         batch_size=50000)

tknzr = Tokenizer.MyTweetTokenizer()
preProcesser = PreProcess.PreProcessor(tknzr.tokenize)

consumer = KafkaConsumer(config[section]['raw_topic'],
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest', enable_auto_commit=True,
                         consumer_timeout_ms=600000)
for message in consumer:
    url_lst = [item['expanded_url'] for item in message.value['entities']['urls']]
    tweet = preProcesser.process(message.value)
    if tweet:
        if args.url:
            url_titles = pageCrawler.pageCrawler(url_lst)
        else:
            url_titles = []

        tweet['crawled_pages'] = url_titles
        producer.send(config[section]['processed_topic'], tweet)
    if message.offset % 500 == 0:
        logger.info("PreProcessed {} messages".format(message.offset))
        logger.info("Sample processed tweet: {}".format(tweet))


