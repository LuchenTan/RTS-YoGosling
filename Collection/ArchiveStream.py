"""
This module is for reading from archive files and acting like a stream.
"""
import bz2
import json
import os
import shutil
import sys
import tarfile
import time
import logging
from kafka import KafkaProducer
from os import path
import configparser
config_path = path.join(path.dirname(__file__), '../config/producer.ini')
config = configparser.ConfigParser()
config.read(config_path)

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         batch_size=int(config['ARCHIVE']['batchsize']))
kafkaTopic = config['ARCHIVE']['raw_topic']
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# offsets = subprocess.check_output(["kafka-run-class.sh", "kafka.tools.GetOffsetShell","--broker-list=localhost:9092", "--topic=" + kafkaTopic]).decode("UTF-8")
# offset = int(offsets.split("\n")[0].split(":")[-1])
# print("Current offset:" + str(offset))
#
# with open('last_offset.txt', 'w') as f:
#     f.write(str(offset))

class ArchiveStream():
    def __init__(self, archive_path):
        self.path = archive_path
        self.tmp_path = "tmp_dir"

    def extract(self, lang=config['LANGUAGE']['lang'], tmp_path=""):
        if tmp_path:
            self.tmp_path = tmp_path
        if self.path.endswith(".tar"):
            tar = tarfile.open(self.path, "r")
            tar.extractall(self.tmp_path)
        elif os.path.isdir(self.path):
            for t in os.listdir(self.path):
                try:
                    tar = tarfile.open(os.path.join(self.path, t), "r")
                    tar.extractall(self.tmp_path)
                # TODO: need to be changed for different input formats
                except:
                    self.tmp_path = self.path
                    pass
        else:
            logger.error("Please input a tar file path or a directory with tar files or bz files")
            shutil.rmtree(self.tmp_path)
            sys.exit(1)
        for root, dirs, files in os.walk(self.tmp_path):
            dirs.sort(key=int)
            files.sort(key=lambda x: int(x.split(".")[0]))
            for file in files:
                if file.endswith(".bz2"):
                    logger.info("Start working on file: {}".format(os.path.join(root, file)))
                    sys.stdout.flush()
                    with bz2.BZ2File(os.path.join(root, file), "r") as bz_file:
                        for line in bz_file:
                            tweet = json.loads(line.decode('utf-8'))
                            if 'text' in tweet and 'lang' in tweet:
                                if lang:
                                    if tweet['lang'] == lang:
                                        try:
                                            if int(config['ARCHIVE']['startpoint']) <= int(tweet['timestamp_ms']) <= int(config['ARCHIVE']['endpoint']):
                                                producer.send(kafkaTopic, tweet)
                                        except:
                                            pass
                                else:
                                    try:
                                        producer.send(kafkaTopic, tweet)
                                    except:
                                        pass
        # clean up
        shutil.rmtree(self.tmp_path)
        logger.info(producer.metrics())


if __name__ == '__main__':
    arcS = ArchiveStream(config['ARCHIVE']['location'])
    start = time.time()
    arcS.extract()
    print("Total time used: ", time.time() - start)
