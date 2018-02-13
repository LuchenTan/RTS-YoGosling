"""
This module is for reading TREC profile file specially.
"""
import json


class TRECProfileReader:
    def __init__(self, path, year):
        self.path = path
        self.year = year
        self.topics = dict()

    def read(self):
        with open(self.path) as fin:
            if self.year in [16, 2016, '16', '2016', 'RTS16']:
                try:
                    for i, line in enumerate(fin.readlines()[1:-1]):
                        if i % 5 == 0:
                            topid = line.split("\" : \"")[1][0:-3]
                        elif i % 5 == 1:
                            title = line.split("\" : \"")[1][0:-3]
                        elif i % 5 == 2:
                            description = line.split("\" : \"")[1][0:-3]
                        elif i % 5 == 3:
                            narr = line.split("\" : \"")[1][0:-2]
                            self.topics[topid] = {"topid": topid, "title": title,
                                             "description": description, "narrative": narr}
                except:
                    print("Please correctly input and match the file path and RTS year!")
            if self.year in [17, 2017, '17', '2017', 'RTS17']:
                try:
                    for i, line in enumerate(fin.readlines()):
                        topic = json.loads(line)
                        self.topics[topic['topid']] = topic
                except:
                    print("Please correctly input and match the file path and RTS year!")

# r = TRECProfileReader("../profiles/TREC2016-RTS-topics.json", 'RTS17')
# r.read()
# print(len(r.topics))