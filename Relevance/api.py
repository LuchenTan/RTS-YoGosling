import sys
from os import path
import Relevance.simpleTitleMatch as simpleTitleMatch
sys.path.append((path.dirname(path.dirname(path.abspath(__file__)))))


def measure(tweet, query, method, thre):
    if method == 'title':
        return simpleTitleMatch.match(query, tweetJson=tweet)