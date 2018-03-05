''' return true if all the tweet text contains all the titles in query '''

def match(query, tweetJson):
    tweets = tweetJson['normal_words']
    titles = query['title']
    return all(title in tweets for title in titles.keys())
    
