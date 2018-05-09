def countTitle(query, tweet):
    titleTokens = query['title'].keys()
    return len(list(set(titleTokens) & set(tweet['normal_words'])))/len(titleTokens)

