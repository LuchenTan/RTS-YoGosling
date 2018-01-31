# Read from all json files in "twitter-stream-2017-12-30.tar" and output the "text" field of each twitter

import json
import time
import tarfile
import os
import bz2

start = time.time()

tar = tarfile.open("twitter-stream-2017-12-30.tar", "r")
tar.extractall("./test_dir")
#count = 0 Just for Test Purpose
for root, dirs, files in os.walk("./test_dir"):
    for file in files:
        if file.endswith(".bz2"):
        	#print("Start working on file: ", os.path.join(root, file))
        	with bz2.BZ2File(os.path.join(root, file), "r") as bz_file:
        		for line in bz_file:
        			#count = count + 1
        			#print("count:", count)
        			tweet = json.loads(line)
        			tweet_content = tweet.get('text', 'deleted')
        			if (tweet_content != 'deleted'):
        				#tweet_content = tweet_content.split()
        				print(tweet_content)
        				#Tweet_length = len(tweet_content)
        				#print("Tweet length:", Tweet_length)      		

print("Total time used: ", time.time() - start)


