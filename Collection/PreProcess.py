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


class PreProcessor:
    def __init__(self, tokenizer, en_lang=True,
                 ascii_filter=True, ascii_count=3,
                 hashtag_count=5,
                 keep_stopword=False,
                 keep_urls=False, keep_hashtags=True):
        self.tokenizer = tokenizer # tokenizer
        self.en_lang = en_lang # use 'lang' field, 'en' only
        self.ascii_filter = ascii_filter # remove NON-ASCII chars or not
        self.ascii_count = ascii_count # ignore tweet if normal words less than this number
        self.hashtag_count = hashtag_count # ignore tweet if hashtag number greater than this number
        self.keep_urls = keep_urls # keep URLs in cleaned text
        self.keep_stopword = keep_stopword # remove stop words from cleaned text
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
            'numbers': [],
            'emojis': [],
            'crawled_pages': []
        }
        text = tweet_json.get('text')
        timestamp_ms = tweet_json.get('timestamp_ms')
        id = tweet_json.get('id')
        if not text or not timestamp_ms or not id:
            self.new_json = None
            return

        # Language Detection, keep 'en' only
        if self.en_lang:
            if not tweet_json.get('lang') == 'en':
                self.new_json = None
                return

        # set new json format
        self.new_json['id'] = id
        self.new_json['text'] = text
        self.new_json['timestamp_ms'] = timestamp_ms

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
                    self.new_json['normal_words'].append(token)
            elif token_type == 'H':
                self.new_json['hashtags'].append(token)
                if self.keep_hashtags:
                    cleaned_text.append(token)
            elif token_type == 'U':
                self.new_json['urls'].append(token)
                if self.keep_urls:
                    cleaned_text.append(token)
            elif token_type == 'USR':
                self.new_json['mentions'].append(token)
            elif token_type == 'PN':
                self.new_json['numbers'].append(token)
                cleaned_text.append(token)
            elif token_type == 'E':
                self.new_json['emojis'].append(token)
            elif token_type == 'S':
                if self.keep_stopword:
                    cleaned_text.append(token.lower())

        # Simple Trash Detection
        if len(self.new_json['hashtags']) >= self.hashtag_count:
            self.new_json = None
            return
        if len(self.new_json['normal_words']) < self.ascii_count:
            self.new_json = None
            return

        self.new_json['cleaned_text'] = " ".join(cleaned_text)
        return self.new_json





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


