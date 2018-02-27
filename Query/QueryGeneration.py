"""
This module is for generating query json format.
Input: a topic json (for now, is a TREC format profile json.
Output: a topic with different weighted/vectored json

{'title': {}, 'narr+desc': {}, 'expansion': {}}
"""
import nltk.tokenize.casual as NLTK
import string
from nltk.corpus import stopwords

PUNCTUATION = list(string.punctuation)
STOP = stopwords.words('english') + ['rt', 'via']


class QueryGeneration:
    def __init__(self, topic, current_query=None,
                 tokenizer=NLTK.TweetTokenizer(preserve_case=False),
                 stopword=True):
        self.topic = topic
        self.tknz = tokenizer
        # TODO: setField and addField only works for nltk tweet tokenizer for now
        # TODO: might need to add my tweet tokenizer later
        self.stopword = stopword
        if current_query:
            self._query = current_query
        else:
            self._query = {'title': {}, 'narr+desc': {}, 'expansion': {}}
            self.setField(field='title')

    def getQuery(self):
        return self._query

    def addField(self, field, words=[], weights=[]):
        if field.lower().startswith('t'):
            try:
                for i, w in enumerate(words):
                    self._query['title'][w] = weights[i]
            except:
                print("Please input the same number of words and weights")
                raise
        elif field.lower().startswith('n'):
            try:
                for i, w in enumerate(words):
                    self._query['narr+desc'][w] = weights[i]
            except:
                print("Please input the same number of words and weights")
                raise
        elif field.lower().startswith('e'):
            try:
                for i, w in enumerate(words):
                    self._query['expansion'][w] = weights[i]
            except:
                print("Please input the same number of words and weights")
                raise
        else:
            print('Please input a valid field name: title, narr+desc or expansion')
            return

    def setField(self, field, words=[], weights=[]):
        new_dict = dict()
        if field.lower().startswith('t'):
            if len(words) > 0:
                try:
                    for i, w in enumerate(words):
                        new_dict[w] = weights[i]
                    self._query['title'] = new_dict
                except:
                    print("Please input the same number of words and weights")
                    raise
            else:
                title_tokens = self.tknz.tokenize(self.topic['title'])
                if self.stopword:
                    title_tokens = [token for token in title_tokens if token not in PUNCTUATION]
                else:
                    title_tokens = [token for token in title_tokens if token not in PUNCTUATION+STOP]
                self._query['title'] = {token: 1 for token in title_tokens}
        elif field.lower().startswith('n'):
            try:
                for i, w in enumerate(words):
                    new_dict[w] = weights[i]
                self._query['narr+desc'] = new_dict
            except:
                print("Please input the same number of words and weights")
                raise
        elif field.lower().startswith('e'):
            try:
                for i, w in enumerate(words):
                    new_dict[w] = weights[i]
                self._query['expansion'] = new_dict
            except:
                print("Please input the same number of words and weights")
                raise
        else:
            print('Please input a valid field name: title, narr+desc or expansion')
            return


# import Query.TRECProfile as trec
#
# r = trec.TRECProfileReader("../profiles/TREC2016-RTS-topics.json", 'RTS16')
# r.read()
# for topid, topic in r.topics.items():
#     print(topic['title'])
#     qg = QueryGeneration(topic, {'title': {}, 'narr+': {'a': 1}, 'e': {'b': 1}}, stopword=False)
#     qg.setField('na', ['a', 'b', 'c'], [1, 2, 5])
#     print(qg.getQuery())
