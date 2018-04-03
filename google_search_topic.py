from google import google
num_page = 1

class GoogleSearch:
	def google_search_topic(topic):
		search_results = google.search(topic, num_page)
		for result in search_results:
			print(result.description)
			print("\n")



