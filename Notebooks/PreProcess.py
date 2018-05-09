"""
The module for fast pre-process tweets.
Input: a tweet json structure from stream or archive.
Output: formatted tweet json or None



1. Clean up
    * take all normal words, hashtags, and urls
    * change to lower case
2. Trash filter
    * #hashtags >= 5
    * ASCII normal words greater than 3
3. Format
    * write all useful fields to a json format
"""

class PreProcessor:
    def __init__(self,
                 ascii_filter=True, ascii_count=3,
                 hashtag_count=5,
                 stopword=True,
                 keep_urls=False, keep_hashtags=True):

        self.ascii_filter = ascii_filter # remove NON-ASCII chars or not
        self.ascii_count = ascii_count # ignore tweet if normal words less than this number
        self.hashtag_count = hashtag_count # ignore tweet if hashtag number greater than this number
        self.keep_urls = keep_urls # keep URLs in cleaned text
        self.stopword = stopword # remove stop words from cleaned text
        self.keep_hashtags = keep_hashtags # keep hashtags in cleaned text


    def process(self, tweet_json):
        self.new_json = {
            'id': 0,
            'text': "",
            'timestamp_ms': 0,
            'cleaned_text': "",
            'normal_words': [],
            'hashtags': [],
            'urls': [],
            'mentions': [],
            'emojis': [],
            'crawled_pages': []
        }
        text = tweet_json.get('text')
        timestamp_ms = tweet_json.get('timestamp_ms')
        id = tweet_json.get('id')
        if not text or not timestamp_ms or not id:
            self.new_json = None
            return

        # set new json format
        self.new_json['id'] = id
        self.new_json['text'] = text
        self.new_json['timestamp_ms'] = timestamp_ms

        # Tweet's 'entities' structure
        """
        "entities": {
            "hashtags": [
                {
                  "indices": [
                    32,
                    38
                  ],
                  "text": "nodejs"
                }
            ],
            "urls": [
                {
                  "indices": [
                    32,
                    52
                  ],
                  "url": "http://t.co/IOwBrTZR",
                  "display_url": "youtube.com/watch?v=oHg5SJ…",
                  "expanded_url": "http://www.youtube.com/watch?v=oHg5SJYRHA0"
                }
            ],
            "user_mentions": [
                 {
                  "name": "Twitter API",
                  "indices": [
                    4,
                    15
                  ],
                  "screen_name": "twitterapi",
                  "id": 6253282,
                  "id_str": "6253282"
                }
            ],
            "symbols": [
            ], 
            "media": [
            ]
          }

        """

        # 这个方法有问题，不能改变text长度来取index，但循环里有不能一直改变clean text
        cleaned_text = text
        if 'entities' in tweet_json:
            entities = tweet_json.get('entities')
            if 'hashtags' in entities and len(entities['hashtags']) > 0:
                for hashtag in entities['hashtags']:
                    self.new_json['hashtags'].append(hashtag['text'])
                    if not self.keep_hashtags:
                        cleaned_text = text[:hashtag['indices'][0]] + '$HASHTAG$' + text[hashtag['indices'][1]:]
            if 'urls' in entities and len(entities['urls']) > 0:
                for url in entities['urls']:
                    self.new_json['urls'].append(url['expanded_url'])
                    if not self.keep_urls:
                        cleaned_text = text[:url['indices'][0]] + '$URL$' + text[url['indices'][1]:]
            if 'user_mentions' in entities and len(entities['user_mentions']) > 0:
                for mention in entities['user_mentions']:
                    self.new_json['mentions'].append(mention['screen_name'])
                    cleaned_text = text[:mention['indices'][0]] + '$MENTION$' + text[mention['indices'][1]:]
            for key, values in entities.items():
                if key not in ['hashtags', 'urls', 'user_mentions']:
                    for v in values:
                        if 'indices' in v:
                            cleaned_text = text[:v['indices'][0]] + '$ENTITY$' + text[v['indices'][1]:]
        self.new_json['cleaned_text'] = cleaned_text

        # # split token types into different categories
        # cleaned_text = []
        # for (token, token_type) in tokens:
        #     if token_type == 'N':
        #         token = token.lower()
        #         if self.ascii_filter:
        #             token = token.encode("ascii", errors="ignore").decode()
        #         if len(token) > 0:
        #             cleaned_text.append(token)
        #             self.new_json['normal_words'].append(token)
        #     elif token_type == 'H':
        #         self.new_json['hashtags'].append(token)
        #         if self.keep_hashtags:
        #             cleaned_text.append(token)
        #     elif token_type == 'U':
        #         self.new_json['urls'].append(token)
        #         if self.keep_urls:
        #             cleaned_text.append(token)
        #     elif token_type == 'USR':
        #         self.new_json['mentions'].append(token)
        #     elif token_type == 'PN':
        #         self.new_json['numbers'].append(token)
        #         cleaned_text.append(token)
        #     elif token_type == 'E':
        #         self.new_json['emojis'].append(token)
        #     elif token_type == 'S':
        #         if self.stopword:
        #             cleaned_text.append(token.lower())

        # Simple Trash Detection
        if len(self.new_json['hashtags']) >= self.hashtag_count:
            self.new_json = None
            return
        # if len(self.new_json['normal_words']) < self.ascii_count:
        #     self.new_json = None
        #     return


        return self.new_json

