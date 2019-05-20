import pymongo
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class RetrieveInvertedIndex:
	def __init__(self):
		# Load the list of english stopwords
		self.english_stopwords = stopwords.words('english')

		# Establishing database connection
		self.client = MongoClient('localhost', 27017)
		self.db = client['grant_search']
		self.collection_index = db['inverted_index']

	# To process query and clean it up before being fed to the retriever function
	def process_query(self, query):
		query = word_tokenize(query)
		query = [word.lower() for word in query if word not in english_stopwords]

		return query


	def retrieve_query_results(self, query, topk=10):
		query = process_query(query)

		if len(query) == 0:
			return []

		ids_table_names = []; res_cnt = {}
		for word in query:
			records = self.collection_index.find({"word":word})
			for rec in records:
				if rec is not None:
					ids_table_names = rec['index_list']
					ids_table_names = map(tuple, ids_table_names)

					for id_table_name in ids_table_names:
						if id_table_name not in res_cnt:
							res_cnt[id_table_name] = 1
						else:
							res_cnt[id_table_name] += 1

		res = sorted(res_cnt.items(), key=lambda kv: kv[1], reverse=True)
		res = [id_table_name for id_table_name, cnt in res[:topk]]

		print("Done with sorting")

		return res


# if __name__ == "__main__":
# 	# Load the list of english stopwords
# 	english_stopwords = stopwords.words('english')

# 	# Establishing database connection
# 	client = MongoClient('localhost', 27017)
# 	db = client['grant_search']
# 	collection_index = db['inverted_index']
		
# 	# Testing the query retrieval function
# 	# query = "evaluate the role of the splanchnic bed in epinephrine-induced glucose intolerance"
# 	query = "psychosocial experiences of women with breast cancer across the lifespan"
	
# 	query = process_query(query)

# 	results_of_query = retrieve_query_results(collection_index, query)

# 	print (results_of_query)



