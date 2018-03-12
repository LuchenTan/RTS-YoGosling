from urllib.request import urlopen
from bs4 import BeautifulSoup
import certifi

def pageCrawler(urllist):
	webpageTitle = []
	for url in urllist:
		try:
			#fetch html
			source = urlopen(url, cafile=certifi.where())
			#parse with BeautifulSoup
			BS = BeautifulSoup(source, "html.parser")
			#search for title element, put it into webpageTitle list
			webpageTitle.append(BS.title.string)
		except:
			pass
	return webpageTitle

''' #just for test
het=pageCrawler(["https://www.google.com",
	"https://stackoverflow.com/questions/40975182/importerror-no-module-named-bs4", 
	"https://stackoverflow.com/questions/28859095/most-efficient-method-to-check-if-dictionary-key-exists-and-process-its-value-if", 
	"https://www.reddit.com",
	"https://www.student.cs.uwaterloo.ca/~cs341/",
	"https://www.quora.com/What-is-a-programmers-life-like",
	"https://www.instagram.com"])
print(het)
'''
