"""
This module is for connecting Twitter Public Stream, and write the stream data to Kafka
"""
import json
from twython import TwythonStreamer
from kafka import KafkaProducer
import config.producer_api_config as config
import subprocess

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         batch_size=config.batchsize)
kafkaTopic = config.topic

offsets = subprocess.check_output(["kafka-run-class.sh", "kafka.tools.GetOffsetShell","--broker-list=localhost:9092", "--topic=" + kafkaTopic]).decode("UTF-8")
offset = int(offsets.split("\n")[0].split(":")[-1])
print("Current offset:" + str(offset))

with open('last_offset.txt', 'w') as f:
    f.write(str(offset))

class TwitterStream(TwythonStreamer):

    # def __init__(self, **oauth):
    #    if len(oauth) == 0:
    #        TwythonStreamer(**config.oauth)
    #    else:
    #        TwythonStreamer(**oauth)

    def on_success(self, data):
        if 'text' in data:
            producer.send(kafkaTopic, data)

    def on_error(self, status_code, data):
        print(status_code, "Error received in Kafka producer")
        return True  # Don't kill the stream

    def on_timeout(self):
        return True  # Don't kill the stream

    def get_topic(self):
        return kafkaTopic


if __name__ == '__main__':
    stream = TwitterStream(**config.oauth)
    stream.statuses.sample()

