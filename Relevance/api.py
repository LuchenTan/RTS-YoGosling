import sys
from os import path
import Relevance.simpleTitleMatch as simpleTitleMatch
import Relevance.simpleCounting as simpleCounting
sys.path.append((path.dirname(path.dirname(path.abspath(__file__)))))


def measure(tweet, query, method, thre):
    if method == 'title':
        return simpleTitleMatch.match(query, tweetJson=tweet)
    if method == 'simpleCount':
        return simpleCounting.countTitle(query, tweet, thre)
