def countTitle(query, tweet, threshold):
    titleTokens = query['title'].keys()
    score = len(list(set(titleTokens) & set(tweet['normal_words'])))/float(len(titleTokens))

    if score >= threshold:
        return score
    else:
        return False


