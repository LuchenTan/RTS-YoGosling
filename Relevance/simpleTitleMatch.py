''' return true if all the tweet text contains all the titles in query '''

def match(query, tweetJson):
    tweets = tweetJson['normal_words']
    titles = query['title']
    return all(title in tweets for title in titles.keys())


def match_titles(query, titles):
    query_titles = query['title']
    tokens = []
    for title in titles:
        words = title.split(" ")
        tokens.update(words)
    return all(title in tokens for title in query_titles.keys())
