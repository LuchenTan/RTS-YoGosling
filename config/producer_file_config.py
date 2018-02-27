#!/usr/bin/env python

# kafka topic to write to
topic = 'tweets_archive_2017'

# the number of bytes to batch in memory before writing to kafka (this number should be smaller than your machine's memory)
batchsize = 100000

filename = "/media/l8tan/Data/TweetArchive/RTS2017"

