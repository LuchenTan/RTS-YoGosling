def match(tweet, submissions_lst, thres):
    dup = False
    tweet_words = set(tweet['normal_words'])
    for sub in submissions_lst:
        sub_words = set(sub['normal_words'])
        jaccard = len(tweet_words.intersection(sub_words)) / len(tweet_words.union(sub_words))
        if jaccard > thres:
            dup = True
            break
    return not dup



