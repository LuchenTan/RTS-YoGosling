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
url_parser = parser.add_mutually_exclusive_group(required=False)
url_parser.add_argument('--crawl-url', dest='url', action='store_true',
                        help='indicating crawling the titles of web links in each tweet')
url_parser.add_argument('--no-crawl-url', dest='url', action='store_false',
                        help='indicating not crawling the web link titles')
parser.set_defaults(url=False)

hashtag_parser = parser.add_mutually_exclusive_group(required=False)
hashtag_parser.add_argument('--keep-hashtag', dest='hashtag', action='store_true',
                            help='keeping hashtags in cleaned text')
hashtag_parser.add_argument('--no-keep-hashtag', dest='hashtag', action='store_false',
                            help='removing hashtags in cleaned text')
parser.set_defaults(hashtag=True)

url_clean_parser = parser.add_mutually_exclusive_group(required=False)
url_clean_parser.add_argument('--keep-url', dest='urlClean', action='store_true',
                              help='keeping urls in cleaned text')
url_clean_parser.add_argument('--no-keep-url', dest='urlClean', action='store_false',
                              help='removing urls in cleaned text')
parser.set_defaults(urlClean=False)

stopword_parser = parser.add_mutually_exclusive_group(required=False)
stopword_parser.add_argument('--keep-stopword', dest='stopword', action='store_true',
                            help='keeping stopwords in cleaned text')
stopword_parser.add_argument('--no-keep-stopword', dest='stopword', action='store_false',
                            help='removing stopwords in cleaned text')
parser.set_defaults(stopword=False)

ascii_parser = parser.add_mutually_exclusive_group(required=False)
ascii_parser.add_argument('--ascii-filter', dest='asciiFilter', action='store_true',
                            help='using ASCII filter to remove non-ASCII characters.')
ascii_parser.add_argument('--no-ascii-filter', dest='asciiFilter', action='store_false',
                            help='not using ASCII filter')
parser.set_defaults(asciiFilter=True)

parser.add_argument('--ascii-count', required=False, dest='asciiCount', type=int,
                    help='indicating the number of minimum ASCII tokens after cleaning for junk tweet detection',
                    default=3)

parser.add_argument('--hashtag-count', required=False, dest='hashtagCount', type=int,
                    help='indicating the maximum number of hashtags after cleaning for junk tweet detection',
                    default=5)

args = parser.parse_args()


if args.source == 'archive':
    section = 'ARCHIVE'
elif args.source == 'stream':
    section = 'STREAM'
else:
    section = 'STREAM'  # default

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         batch_size=5000)

tknzr = Tokenizer.MyTweetTokenizer()
preProcesser = PreProcess.PreProcessor(tknzr.tokenize, ascii_filter=args.asciiFilter,
                                       ascii_count=args.asciiCount,
                                       hashtag_count=args.hashtagCount,
                                       keep_stopword=args.stopword,
                                       keep_urls=args.urlClean,
                                       keep_hashtags=args.hashtag)
consumer = KafkaConsumer(config[section]['raw_topic'],
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest', enable_auto_commit=True,
                         consumer_timeout_ms=600000)  # close consumer if no response for 10mins
for message in consumer:
    url_lst = [item['expanded_url'] for item in message.value['entities']['urls']]
    tweet = preProcesser.process(message.value)
    if tweet:
        if args.url:
            url_titles = pageCrawler.pageCrawler(url_lst)
            tweet['crawled_pages'] = url_titles
            producer.send(config[section]['processed_topic_crawled'], tweet)
        else:
            producer.send(config[section]['processed_topic_nocrawl'], tweet)
    if message.offset % 5000 == 0:
        logger.info("PreProcessed {} messages".format(message.offset))
        logger.info("Sample processed tweet: {}".format(tweet))


