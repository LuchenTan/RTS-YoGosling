# Read from all json files in "twitter-stream-2017-12-30.tar" and output the "text" field of each twitter

import json
import time
import tarfile
import os
import bz2
import sys
from kafka import KafkaProducer
import config.producer_file_config as config

start = time.time()

topic = config.topic
batchsize = config.batchsize
filename = config.filename

arglen = len(sys.argv)

if arglen > 1:
    topic = argv[1]
    if arglen > 2:
        batchsize = argv[2]

producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), batch_size=batchsize)

tar = tarfile.open(filename, "r")
tar.extractall("./test_dir")
count = 0
for root, dirs, files in os.walk("./test_dir"):
    for file in files:
        if file.endswith(".bz2"):
        	print("Start working on file: ", os.path.join(root, file))
        	with bz2.BZ2File(os.path.join(root, file), "r") as bz_file:
        		for line in bz_file:
				tweet = json.loads(line)
        			tweet_content = tweet.get('text', 'deleted')
        			if (tweet_content != 'deleted'):
                                        producer.send(topic, tweet) 

print("Total time used: ", time.time() - start)


metrics = producer.metrics()
print(json.dumps(metrics, indent=4))

