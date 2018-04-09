import json
from google import google

num_page = 1

topic16_file = 'profiles/TREC2016-RTS-topics.json'
topic17_file = 'profiles/RTS17-topics.json'


with open('profiles/RTS17-topics.json', encoding='utf-8') as topic_file:
	#print(topic_file.read())
	for line in topic_file:
		topic = json.loads(line)
		#print(topic)
		topic_title = topic.get('title', '')
		topic_id = topic.get('topid', '')
		topic_search_result = {}
		descriptions = []
		search_results = google.search(topic_title, num_page)
		for result in search_results:
			try:
				if (result.description):
				    descriptions.append(result.description)
			except Exception as e:
				pass
		topic_search_result['topid'] = topic_id
		topic_search_result['descriptions'] = descriptions

		with open('topic_descriptions.json', 'a') as outfile:
			json.dump(topic_search_result, outfile)
			outfile.write("\n")

	



