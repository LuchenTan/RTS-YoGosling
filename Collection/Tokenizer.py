import nltk.tokenize.casual as NLTK
import re
from nltk.corpus import stopwords
import string

PUNCTUATION = list(string.punctuation)
STOP = stopwords.words('english') + ['rt', 'via']

##########################################
# These are the core regular expressions.
# Copied from nltk.tokenize.casual, but separate to different types.
##########################################

EMOTICONS = NLTK.EMOTICONS
EMOJIS = r"""[\U00010000-\U0010ffff]"""

URLS = NLTK.URLS

Phone_numbers = r"""
    (?:
      (?:            # (international)
        \+?[01]
        [\-\s.]*
      )?
      (?:            # (area code)
        [\(]?
        \d{3}
        [\-\s.\)]*
      )?
      \d{3}          # exchange
      [\-\s.]*
      \d{4}          # base
    )"""

Username = r"""
(?:@[\w_]+)"""

Hashtags = r"""
(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""

Email = r"""
[\w.+-]+@[\w-]+\.(?:[\w-]\.?)+[\w-]"""

# The components of the tokenizer:
REGEXPS = NLTK.REGEXPS
# Modified from nltk regexps. Separated different types.
NormWords = (
    # HTML tags:
    r"""<[^>\s]+>"""
    ,
    # ASCII Arrows
    r"""[\-]+>|<[\-]+"""
    ,
    # Remaining word types:
    r"""
    (?:[^\W\d_](?:[^\W\d_]|['\-_])+[^\W\d_]) # Words with apostrophes or dashes.
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots.
    |
    (?:\S)                         # Everything else that isn't whitespace.
    """
    )

######################################################################
# This is the core tokenizing regex:

WORD_RE = re.compile(r"""(%s)""" % "|".join(REGEXPS), re.VERBOSE | re.I
                     | re.UNICODE)

# WORD_RE performs poorly on these patterns:
HANG_RE = re.compile(r"""([^a-zA-Z0-9])\1{3,}""")

# The emoticon string gets its own regex so that we can preserve case for
# them as needed:
EMOTICON_RE = re.compile(EMOTICONS, re.VERBOSE | re.I | re.UNICODE)

# These regex are added
EMOJI_RE = re.compile(EMOJIS, re.UNICODE)
URLS_RE = re.compile(URLS, re.VERBOSE | re.I | re.UNICODE)
PHONUM_RE = re.compile(Phone_numbers, re.VERBOSE | re.I | re.UNICODE)
USERNAME_RE = re.compile(Username, re.VERBOSE | re.I | re.UNICODE)
HASHTAG_RE = re.compile(Hashtags, re.VERBOSE | re.I | re.UNICODE)
EMAIL_RE = re.compile(Email, re.VERBOSE | re.I | re.UNICODE)
NORMAL_RE = re.compile(r"""(%s)""" % "|".join(NormWords), re.VERBOSE | re.I | re.UNICODE)
class MyTweetTokenizer:
    r"""
    Modified from nltk TweetTokenizer
    If type argument is set to be True,
    Return a tuple for each token, with the token and its type.
    Otherwise,
    Return the original nltk TweetTokenizer results.
    Type codes:
    N: normal words
    E: emoticons or emojis
    U: urls or emails
    PN: phone number
    USR: user names
    H: hashtags
    S: stopwords
    PUNC: punctuations
    """

    def __init__(self, type_include=True):
        self.type_include = type_include

    def tokenize(self, text):
        if not self.type_include:
            tknzr = NLTK.TweetTokenizer()
            return tknzr.tokenize(text)

        # Fix HTML character entities:
        text = NLTK._replace_html_entities(text)
        # Shorten problematic sequences of characters
        safe_text = NLTK.HANG_RE.sub(r'\1\1\1', text)
        # Tokenize:
        words = WORD_RE.findall(safe_text)

        # # Possibly alter the case, but avoid changing emoticons like :D into :d:
        for i, x in enumerate(words[:]):

            if EMOTICON_RE.match(x) or EMOJI_RE.match(x):
                words[i] = (x, 'E')
            elif URLS_RE.match(x) or EMAIL_RE.match(x):
                words[i] = (x, 'U')
            elif USERNAME_RE.match(x):
                words[i] = (x, 'USR')
            elif HASHTAG_RE.match(x):
                words[i] = (x, 'H')
            elif PHONUM_RE.match(x):
                words[i] = (x, 'PN')
            elif x.lower() in STOP:
                words[i] = (x, 'S')
            elif x in PUNCTUATION:
                words[i] = (x, 'PUNC')
            else:
                words[i] = (x, 'N')
        return words

# tz = MyTweetTokenizer()
# t ="RT @team_staystrong: #np COOL FOR THE SUMMER #DemiLovato"
# print(tz.tokenize(t))