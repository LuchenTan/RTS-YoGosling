from Collection import Tokenizer, PreProcess
from Query import QueryGeneration, TRECProfile
from Relevance import simpleCounting as rm
import json

# Load Profiles
rts16_path = "profiles/TREC2016-RTS-topics.json"
rts17_path = "profiles/RTS17-topics.json"
profile = TRECProfile.TRECProfileReader(rts17_path, 17)
profile.read()
queryset = dict()
for topid, topic in profile.topics.items():
    queryset[topid] = QueryGeneration.QueryGeneration(topic).getQuery()



# Load Tweets
tknzr = Tokenizer.MyTweetTokenizer()
prePro = PreProcess.PreProcessor(tknzr.tokenize)
path = "/media/l8tan/Data/30.json"
with open(path) as fin:
    for i, line in enumerate(fin.readlines()):
        tweet = json.loads(line)
        tweetjson = prePro.process(tweet)
        if tweetjson:
            print(tweetjson['text'])
            for topid, query in queryset.items():
                score = rm.countTitle(query, tweetjson)
                if score > 0:
                    print(topid, query['title'], score)

