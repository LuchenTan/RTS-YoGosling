import sys
from os import path
import Similarity.Jaccard as Jaccard
sys.path.append((path.dirname(path.dirname(path.abspath(__file__)))))


def measure(tweet, submissions_lst, method, thres):
    if method == 'jaccard':
        return Jaccard.match(tweet, submissions_lst, thres)