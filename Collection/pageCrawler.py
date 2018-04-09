from urllib.request import urlopen
from bs4 import BeautifulSoup
import certifi
import logging
import signal


def CrawlSingleUrl(url):
	#fetch html
	source = urlopen(url, cafile=certifi.where())
	#parse with BeautifulSoup
	BS = BeautifulSoup(source, "html.parser")
	#print(BS.title.string)
	return BS.title.string


def timeout(url, timeout_duration=10, default=None):
    class TimeoutError(Exception):
        pass
    def handler(signum, frame):
        raise TimeoutError()
    # set the timeout handler
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(timeout_duration)
    try:
        result = CrawlSingleUrl(url)
    except TimeoutError as exc:
        result = ''
    finally:
        signal.alarm(0)
    return result


def pageCrawler(urllist):
	webpageTitle = []
	for url in urllist:
		try:
			result=timeout(url)
			if result:
				webpageTitle.append(result)
		except Exception as e:
			pass
	#print(webpageTitle)
	return webpageTitle


'''	
#just for test
het=["https://www.google.com",
	"https://stackoverflow.com/questions/40975182/importerror-no-module-named-bs4", 
	"https://stackoverflow.com/questions/28859095/most-efficient-method-to-check-if-dictionary-key-exists-and-process-its-value-if", 
	"https://www.reddit.com",
	"https://www.student.cs.uwaterloo.ca/~cs341/",
	"https://www.quora.com/What-is-a-programmers-life-like",
	"https://learn.uwaterloo.ca/d2l/le/content/362760/viewContent/2078244/View?ou=362760",
	"https://www.student.cs.uwaterloo.ca/~cs350/W18/assignments/a2a.pdf",
	"https://en.wikipedia.org/wiki/Edward_the_Confessor",
	"https://en.wikipedia.org/wiki/Turing_machine",
	"https://en.wikipedia.org/wiki/Model_of_computation",
	"https://en.wikipedia.org/wiki/Finite-state_machine",
	"https://en.wikipedia.org/wiki/Directed_graph",
	"www.youtube.com/channel/UCzGJNfa_jMx-QmOZ87hYyIg",
	"twitter.com/a_better_Gozo",
	"https://www.kijiji.ca",
	"https://t.co/8laH4lcRQJ",
	"https://www.instagram.com"]
pageCrawler(het)
'''
