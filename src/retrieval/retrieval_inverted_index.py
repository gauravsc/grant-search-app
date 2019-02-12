import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def process_query(inverted_idx, query, english_stopwords, topk=10):
	query_words = word_tokenize(query)
	query_words = [word for word in query_words if word not in english_stopwords]

	if len(query_words) == 0:
		return []

	pmids = []
	for word in query_words:
		pmids += inverted_idx[word]

	res_cnt = {}
	for pmid in pmids:
		if pmid not in res_cnt:
			res_cnt[pmid] = 1
		else:
			res_cnt[pmid] += 1

	res = sorted(res_cnt.items(), key=lambda kv: kv[1], reverse=True)
	res = [pmid for pmid, cnt in res[:topk]]

	return res


if __name__ == "__main__":
	
	# Declaring and loading some global variables	
	path = '../data/inverted_idx.json'
	english_stopwords = stopwords.words('english')
	inverted_idx = json.load(open(path, 'r')) 

	# Testing the query retrieval function
	# query = "evaluate the role of the splanchnic bed in epinephrine-induced glucose intolerance"
	query = "psychosocial experiences of women with breast cancer across the lifespan"
	results_of_query = process_query(inverted_idx, query, english_stopwords)

	print (results_of_query[:7])



