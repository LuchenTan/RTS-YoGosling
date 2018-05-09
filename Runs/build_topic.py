import argparse
import logging
import sys
from subprocess import Popen, PIPE, STDOUT
import Collection.TwitterStream as stream
import Collection.ArchiveStream as archive
from os import path
import configparser
sys.path.append((path.dirname(path.dirname(path.abspath(__file__)))))
config_path = path.join(path.dirname(__file__), '../config/producer.ini')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# setup arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', choices=set(('stream', 'archive')),
                    help='indicating input source using term "stream" or "archive". '
                         'stream for listening Twitter Streaming API;'
                         'archive for reading from files on disk.',
                    required=True)

args = parser.parse_args()

# read configuration file
config = configparser.ConfigParser()
config.read(config_path)


if args.source == 'archive':
    section = 'ARCHIVE'
elif args.source == 'stream':
    section = 'STREAM'
else:
    section = 'STREAM'  # default

# clean all topics
topic_lst = ['raw_topic', 'processed_topic']
for topic in topic_lst:
    process = Popen('./bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic {}'.format(config[section][topic]),
                    stdout=PIPE, stderr=STDOUT, shell=True, cwd=config['Kafka']['path'])
    process_output, _ = process.communicate()
    logger.info("Attempt to delete topic {}".format(config[section][topic]))
    if 'does not exist' in str(process_output) or 'is marked for deletion' in str(process_output):
        pass
    else:
        logger.error('Could not delete topic {}! Please try to select a different topic name.'.format(topic))
        sys.exit(1)
    exitcode = process.wait()
    logger.info("{} has been deleted!".format(config[section][topic]))

# produce raw tweet topic
logger.info("Auto create new topic {}".format(config[section]['raw_topic']))
if args.source == 'archive':
    arcS = archive.ArchiveStream(config['ARCHIVE']['location'])
    arcS.extract()
else:
    streamS = stream.TwitterStream(**dict(config['OAUTH']))
    streamS.statuses.sample()


#
# from kafka import KafkaConsumer
#
# consumer = KafkaConsumer(config['ARCHIVE']['raw_topic'],
#                             bootstrap_servers=['localhost:9092']
#                             ,auto_offset_reset='earliest', enable_auto_commit=True)
# for message in consumer:
#     # message value and key are raw bytes -- decode if necessary!
#     # e.g., for unicode: `message.value.decode('utf-8')`
#     print("%s:%d:%d: key=%s" % (message.topic, message.partition,
#                                 message.offset, message.key))


# from kafka import SimpleClient
#
# client = SimpleClient('localhost:9092')
# topic_partition_ids = client.get_partition_ids_for_topic(config['ARCHIVE']['raw_topic'])
# print(topic_partition_ids)
