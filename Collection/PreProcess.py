"""
The module for fast pre-process tweets.
Input: a tweet json structure from stream or archive.
Output: formatted tweet json or None

NOTE:
    The PreProcessor.process depends on the modified
    tokenizer with types included.

1. Language filter:
    * 'lang' field from tweet json
2. Clean up
    * take all normal words, hashtags, and urls
    * change to lower case
3. Trash filter
    * #hashtags >= 5
    * ASCII normal words greater than 3
4. Format
    * write all useful fields to a json format
"""
import json

class PreProcessor:
    def __init__(self, tokenizer, en_lang=True,
                 ascii_filter=True, ascii_count=3,
                 hashtag_count=5,
                 stopword_remove=False,
                 keep_urls=True, keep_hashtags=True):
        self.tokenizer = tokenizer # tokenizer
        self.en_lang = en_lang # use 'lang' field, 'en' only
        self.ascii_filter = ascii_filter # remove NON-ASCII chars or not
        self.ascii_count = ascii_count # ignore tweet if normal words less than this number
        self.hashtag_count = hashtag_count # ignore tweet if hashtag number greater than this number
        self.keep_urls = keep_urls # keep URLs in cleaned text
        self.stopword_remove = stopword_remove # remove stop words from cleaned text
        self.keep_hashtags = keep_hashtags # keep hashtags in cleaned text

    def process(self, tweet_json):
        text = tweet_json.get('text')
        timestamp_ms = tweet_json.get('timestamp_ms')
        id = tweet_json.get('id')
        if not text or not timestamp_ms or not id:
            return None

        # Language Detection, keep 'en' only
        if self.en_lang:
            if not tweet_json.get('lang') == 'en':
                return None

        # built new json format
        new_json = {
            'id': id,
            'text': text,
            'timestamp_ms': timestamp_ms,
            'cleaned_text': "",
            'normal_words': [],
            'hashtags': [],
            'urls': [],
            'mentions': [],
            'numbers': [],
            'emojis': [],
            'crawled_pages': []
        }
        # Tokenization
        tokens = self.tokenizer(text)

        # split token types into different categories
        cleaned_text = []
        for (token, token_type) in tokens:
            if token_type == 'N':
                token = token.lower()
                if self.ascii_filter:
                    token = token.encode("ascii", errors="ignore").decode()
                if len(token) > 0:
                    cleaned_text.append(token)
                    new_json['normal_words'].append(token)
            elif token_type == 'H':
                new_json['hashtags'].append(token)
                if self.keep_hashtags:
                    cleaned_text.append(token)
            elif token_type == 'U':
                new_json['urls'].append(token)
                if self.keep_urls:
                    cleaned_text.append(token)
            elif token_type == 'USR':
                new_json['mentions'].append(token)
            elif token_type == 'PN':
                new_json['numbers'].append(token)
                cleaned_text.append(token)
            elif token_type == 'E':
                new_json['emojis'].append(token)
            elif token_type == 'S':
                if not self.stopword_remove:
                    cleaned_text.append(token.lower())

        # Simple Trash Detection
        if len(new_json['hashtags']) >= self.hashtag_count:
            return None
        if len(new_json['normal_words']) < self.ascii_count:
            return None

        new_json['cleaned_text'] = " ".join(cleaned_text)
        return new_json


# import Collection.Tokenizer as tt
# tkr = tt.MyTweetTokenizer()
# ppr = PreProcessor(tkr.tokenize)
# path = "/media/l8tan/Data/30.json"
# with open(path) as fin:
#     for i, line in enumerate(fin.readlines()):
#         tweet = json.loads(line)
#
#         print(tweet.get('text'))
#         print(ppr.process(tweet))
#         print("################################33")


