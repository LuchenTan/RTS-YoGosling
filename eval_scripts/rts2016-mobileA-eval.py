#!/usr/bin/python

# This is the evaluation script for the TREC 2016 RTS evaluation
# (scenario A) with mobile assessor judgments, v1.01.
#
# Release History:
#
# - v1.01 (Dec 2016):
#     + Computes latency per topic. Latency is computed with respect
#       to the pushed tweet. Note "All" latency (aggregate over all
#       topics) is a MICRO-average.
#     + Output is tab-delimited instead of space-delimited.
#
# - v1.00 (Oct 2016): Original release

__author__ = 'Luchen Tan'
import numpy
import argparse
import sys

evaluation_starts = 1470096000
evaluation_ends = 1470960000
seconds_perday = 86400
K = 10

# We discovered that, from the RTS evaluation broker's perspective,
# some tweets were pushed before they were actually posted on
# Twitter. Since it is unlikely that participants had created time
# traveling devices, we attributed the issue to clock skew on the
# broker. Note that since the broker was an EC2 instance, there is no
# way to debug post hoc. The only reasonable solution we could come up
# with was to add a temporal offset to *all* pushed tweets. We set
# this offset to 139 seconds, the maximum gap between a system push
# time and the created time of the tweet.
#
# NOTE: This effectively sets an upper bound on the temporal
# resolution when interpreting system latencies.
time_travel = 139  # time travel in seconds

parser = argparse.ArgumentParser(description='Evaluation script for TREC 2016 RTS scenario A with mobile assessor judgments')
parser.add_argument('-q', required=True, metavar='qrels', help='qrels file')
parser.add_argument('-r', required=True, metavar='run', help='run file')
parser.add_argument('-t', required=True, metavar='tweetsdayepoch', help='tweets2dayepoch file')

args = parser.parse_args()
file_qrels_path = vars(args)['q']
run_path = vars(args)['r']
file_tweet2day = vars(args)['t']

qrels_dt = {}
for i, line in enumerate(open(file_qrels_path)):
    line = line.strip().split()
    topic = line[0]
    tweetid = line[1]
    judgement = int(line[3])
    if topic not in qrels_dt:
        qrels_dt[topic] = {'rel': [], 'redundant': [], 'non_rel': [], 'all_judged': []}
    if judgement == 2:
        if tweetid not in qrels_dt[topic]['rel']:
            qrels_dt[topic]['rel'].append(tweetid)
    elif judgement == 1:
        if tweetid not in qrels_dt[topic]['redundant']:
            qrels_dt[topic]['redundant'].append(tweetid)
    else:
        if tweetid not in qrels_dt[topic]['non_rel']:
            qrels_dt[topic]['non_rel'].append(tweetid)
    if tweetid not in qrels_dt[topic]['all_judged']:
        qrels_dt[topic]['all_judged'].append(tweetid)

# created timestamp and date for each tweetid in the qrel
# tweet2day_dt: {tweetid: date}
# tweet2epoch_dt: {tweetid: epoch time}
tweet2day_dt = {}
tweet2epoch_dt = {}
for line in open(file_tweet2day).readlines():
    line = line.strip().split()
    tweet2day_dt[line[0]] = line[1]
    tweet2epoch_dt[line[0]] = line[2]


# run dictionaries
# run_dt: {topic: {date: [tweetids}}
# run_epoch_dt: {topic: {tweetid: adjusted epoch time}}
runname = ''
run_dt = {}
run_epoch_dt = {}
for line in open(run_path).readlines():
    line = line.strip().split()
    runname = line[3]
    topic = line[0]
    push_time = int(line[2])
    if topic in qrels_dt:
        tweetid = line[1]

        if topic not in run_dt:
            run_dt[topic] = {}
            run_epoch_dt[topic] = {}
        day = (push_time - evaluation_starts) / seconds_perday
        if 0 <= day < 10:
            if topic in run_dt:
                if day in run_dt[topic]:
                    run_dt[topic][day].append(tweetid)
                else:
                    run_dt[topic][day] = [tweetid]
            else:
                run_dt[topic] = {day: [tweetid]}
        # The epoch time of run push is adjusted by the clock offset
        epoch = int(float(line[2])) + int(float(time_travel))
        if tweetid in tweet2day_dt:
            if epoch >= int(tweet2epoch_dt[tweetid]):
                run_epoch_dt[topic][tweetid] = epoch


print("\t".join(["run", "topic", "relevant", "redundant", "not_relevant", "unjudged", "total_length", "mean_latency", "median_latency"]))
total_rel, total_redundant, total_non_rel, total_unjudged, total_length = 0, 0, 0, 0, 0
all_delay = []
missing_tweets = 0
for topic in sorted(qrels_dt.keys()):
    rel, redundant, non_rel, unjudged, length = 0, 0, 0, 0, 0
    delay_list = []
    if topic in run_dt:
        for day in run_dt[topic]:
            length += len(run_dt[topic][day])
            tweets_counted = run_dt[topic][day][:K]
            for tweetid in tweets_counted:
                if tweetid in qrels_dt[topic]['rel']:
                    rel += 1
                if tweetid in qrels_dt[topic]['redundant']:
                    redundant += 1
                if tweetid in qrels_dt[topic]['non_rel']:
                    non_rel += 1
                if tweetid not in qrels_dt[topic]['all_judged']:
                    unjudged += 1

                if tweetid in tweet2day_dt:
                    delay = (int(float(run_epoch_dt[topic][tweetid])) - int(tweet2epoch_dt[tweetid]))
                    delay = max(0, delay)
                    delay_list.append(delay)
                else:
                    missing_tweets += 1
            unjudged += max(0, len(run_dt[topic][day]) - K)
    print("\t".join([runname, topic, str(rel), str(redundant), str(non_rel), str(unjudged), str(length),
                    str(round(numpy.mean(delay_list) if delay_list != [] else 0, 1)),
                    str(round(numpy.median(delay_list) if delay_list != [] else 0, 1))]))
    total_rel += rel
    total_redundant += redundant
    total_non_rel += non_rel
    total_unjudged += unjudged
    total_length += length
    all_delay += delay_list

print("\t".join([runname, "All", str(total_rel), str(total_redundant), str(total_non_rel), str(total_unjudged), str(total_length),
                str(round(numpy.mean(all_delay) if all_delay != [] else 0, 1)),
                str(round(numpy.median(all_delay) if all_delay != [] else 0, 1))]))
print(runname, '# missing tweet ids in the pool', missing_tweets)
