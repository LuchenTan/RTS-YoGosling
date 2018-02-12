#!/usr/bin/env python

# kafka topic to write to
topic = 'tweets_file_2'

# the number of bytes to batch in memory before writing to kafka (this number should be smaller than your machine's memory)
batchsize = 100000

filename = "/media/l8tan/Data/TweetArchive/RTS17/twitter-stream-2017-07-28.tar"

