"""
This module is for connecting Twitter Public Stream, and write the stream data to Kafka
"""
import logging
import json
from twython import TwythonStreamer
from kafka import KafkaProducer
from os import path
import configparser
config_path = path.join(path.dirname(__file__), '../config/producer.ini')
config = configparser.ConfigParser()
config.read(config_path)


producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         batch_size=int(config['STREAM']['batchsize']))
kafkaTopic = config['STREAM']['raw_topic']


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#
# offsets = subprocess.check_output(["kafka-run-class.sh", "kafka.tools.GetOffsetShell","--broker-list=localhost:9092", "--topic=" + kafkaTopic]).decode("UTF-8")
# offset = int(offsets.split("\n")[0].split(":")[-1])
# print("Current offset:" + str(offset))
#
# with open('last_offset.txt', 'w') as f:
#     f.write(str(offset))

class TwitterStream(TwythonStreamer):

    # def __init__(self, **oauth):
    #    if len(oauth) == 0:
    #        TwythonStreamer(**config.oauth)
    #    else:
    #        TwythonStreamer(**oauth)

    def on_success(self, data):
        if 'text' in data and 'lang' in data and \
                        data['lang'] == config['LANGUAGE']['lang']:
            producer.send(kafkaTopic, data)

    def on_error(self, status_code, data):
        logger.error("Error received in Kafka producer, code {}".format(status_code))
        return True  # Don't kill the stream

    def on_timeout(self):
        return True  # Don't kill the stream

    def get_topic(self):
        return kafkaTopic


if __name__ == '__main__':
    stream = TwitterStream(**dict(config['OAUTH']))
    stream.statuses.sample()

