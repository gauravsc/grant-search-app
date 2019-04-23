import pymongo
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import csv
import nltk
import json

request_size = 10000

# Create inverted index of the words
def create_index(abstract_text, _id, table_name, merged_dict):
	word_list = word_tokenize(abstract_text)
	word_list = [word.lower() for word in word_list if word not in english_stopwords]
	
	for word in word_list:
		merged_dict[word].append((_id, table_name))

	return merged_dict


def update_inverted_index(collection_index, temp_inv_idx):
	words_to_update = temp_inv_idx.keys()
	docs_to_insert = []
	for word in words_to_update:
		docs_to_insert.append({'word':word, 'index_list':temp_inv_idx[word]})
	
	collection_index.insert_many(docs_to_insert)
		

# def merge_dictinaries(dict1, dict2):
# 	dict_merged = {}
# 	for key in dict1.keys():
# 		if key in dict2:
# 			dict_merged[key] = dict1[key] + dict2[key]
# 		else:
# 			dict_merged[key] = dict1[key]

# 	for key in dict2.keys():
# 		if key in dict1:
# 			dict_merged[key] = dict1[key] + dict2[key]
# 		else:
# 			dict_merged[key] = dict2[key]

# 	return dict_merged


def index_pubmed_text(db, collection_index):
	collection_pubmed = db['pubmed_info']

	_ids_to_index = [rec['_id'] for rec in collection_pubmed.find({}, { "_id": 1})]
	merged_dict = defaultdict(list)

	for i, _id in enumerate(_ids_to_index):
		try:
			rec = collection_pubmed.find_one({'_id': _id})
			abstract_text = " ".join(rec['Abstract'])
		except KeyError:
			print ("key error continuing ...")
			continue

		merged_dict = create_index(abstract_text, _id, 'pubmed_info', merged_dict)
		print (str(i+1)+'/'+str(len(_ids_to_index)))

		if (i+1) % request_size == 0 or i == len(_ids_to_index)-1:
			update_inverted_index(collection_index, merged_dict)
			merged_dict = defaultdict(list)


def index_NIHRIO_text(db, collection_index):
	collection_nihrio = db['nihrio_info']

	_ids_to_index = [rec['_id'] for rec in collection_nihrio.find({}, { "_id": 1})]
	merged_dict = defaultdict(list)

	for i, _id in enumerate(_ids_to_index):
		try:
			rec = collection_nihrio.find_one({"_id": _id})
			abstract_text = rec['objective']
		except KeyError:
			continue
		
		merged_dict = create_index(abstract_text, _id, 'nihrio_info', merged_dict)
		print (str(i+1)+'/'+str(len(_ids_to_index)))

		if i % request_size == 0 or i == len(_ids_to_index)-1:
			update_inverted_index(collection_index, merged_dict)
			merged_dict = defaultdict(list)


def index_NIHR_text(db, collection_index):
	collection_nihr = db['nihr_info']

	_ids_to_index = [rec['_id'] for rec in collection_nihr.find({}, { "_id": 1})]
	merged_dict = defaultdict(list)

	for i, _id in enumerate(_ids_to_index):
		try:
			rec = collection_nihr.find_one({"_id": _id})
			abstract_text = rec['fields']['plain_english_abstract']
		except KeyError:
			continue
		
		merged_dict = create_index(abstract_text, _id, 'nihr_info', merged_dict)
		print (str(i+1)+'/'+str(len(_ids_to_index)))

		if i % request_size == 0 or i == len(_ids_to_index)-1:
			update_inverted_index(collection_index, merged_dict)
			merged_dict = defaultdict(list)


def index_NLM_text(db, collection_index):
	collection_nlm = db['clinical_trials_NLM_info']

	_ids_to_index = [rec['_id'] for rec in collection_nlm.find({}, { "_id": 1})]
	merged_dict = defaultdict(list)

	for i, _id in enumerate(_ids_to_index):
		try:
			rec = collection_nlm.find_one({"_id": _id})
			abstract_text = rec['clinical_study']['brief_summary']['textblock']
		except KeyError:
			continue

		merged_dict = create_index(abstract_text, _id, 'clinical_trials_NLM_info', merged_dict)
		print (str(i+1)+'/'+str(len(_ids_to_index)))

		if i % request_size == 0 or i == len(_ids_to_index)-1:
			update_inverted_index(collection_index, merged_dict)
			merged_dict = defaultdict(list)


if __name__ == "__main__":
	# Load english stopwords
	english_stopwords = stopwords.words('english')
	
	# Establishing database connection
	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection_index = db['inverted_index']

	collection_index.create_index([('word', pymongo.DESCENDING)])
	# # create inverted index on pubmed info
	index_pubmed_text(db, collection_index)
	# # create inverted index on nihrio info
	index_NIHRIO_text(db, collection_index)
	# # create inverted index on nihr info
	index_NIHR_text(db, collection_index)
	# # create inverted index on nlm info
	index_NLM_text(db, collection_index)



	