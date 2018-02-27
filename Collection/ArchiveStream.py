"""
This module is for reading from archive files and acting like a stream.
"""
import json
import tarfile, bz2
from kafka import KafkaProducer
import config.producer_file_config as config
import os, shutil

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         batch_size=config.batchsize)
kafkaTopic = config.topic


class ArchiveStream():
    def __init__(self, archive_path):
        self.path = archive_path
        self.tmp_path = os.path.join(os.path.dirname(self.path), "tmp_dir")
        print(self.tmp_path)

    def extract(self, tmp_path=""):
        if tmp_path:
            self.tmp_path = tmp_path
        tar = tarfile.open(self.path, "r")
        tar.extractall(self.tmp_path)
        for root, dirs, files in os.walk(self.tmp_path):
            for file in files:
                if file.endswith(".bz2"):
                    print("Start working on file: ", os.path.join(root, file))
                    with bz2.BZ2File(os.path.join(root, file), "r") as bz_file:
                        for line in bz_file:
                            tweet = json.loads(line.decode('utf-8'))
                            if 'text' in tweet and 'lang' in tweet and tweet['lang'] == 'en':
                                try:
                                    producer.send(kafkaTopic, tweet)
                                except:
                                    pass
        # clean up
        shutil.rmtree(self.tmp_path)

if __name__ == '__main__':
    arcS = ArchiveStream(config.filename)
    arcS.extract()