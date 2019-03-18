import pymongo
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import csv
import nltk
import json

# Create inverted index of the words
def create_index(abstract_text, _id, table_name):
	word_list = word_tokenize(abstract_text)
	word_list = [word.lower() for word in word_list if word not in english_stopwords]
	
	temp_inv_idx = defaultdict(list)
	for word in word_list:
		temp_inv_idx[word].append((_id, table_name))

	return temp_inv_idx


def update_inverted_index(collection_index, temp_inv_idx):
	words_to_update = temp_inv_idx.keys()

	for word in words_to_update:
		rec = collection_index.find_one({'word':word})
		if rec is None:
			collection_index.insert_one({'word':word, 'index_list':temp_inv_idx[word]})
		else:
			collection_index.replace_one({'word':word}, {'word':word, 'index_list':temp_inv_idx[word]+rec['index_list']})


def index_pubmed_text(db, collection_index):
	collection_pubmed = db['pubmed_info']

	_ids_to_index = [rec['_id'] for rec in collection_pubmed.find({}, { "_id": 1})]

	for _id in _ids_to_index:
		try:
			rec = collection_pubmed.find_one({'_id': _id})
			abstract_text = " ".join(rec['Abstract'])
		except KeyError:
			print ("key error continuing ...")
			continue

		temp_inv_idx = create_index(abstract_text, _id, 'pubmed_info')
		update_inverted_index(collection_index, temp_inv_idx)


def index_NIHRIO_text(db, collection_index):
	collection_nihrio = db['nihrio_info']

	_ids_to_index = [rec['_id'] for rec in collection_nihrio.find({}, { "_id": 1})]

	for _id in _ids_to_index:
		try:
			rec = collection_nihrio.find_one({"_id": _id})
			abstract_text = rec['objective']
		except KeyError:
			continue
		
		temp_inv_idx = create_index(abstract_text, _id, 'nihrio_info')
		update_inverted_index(collection_index, temp_inv_idx)


def index_NIHR_text(db, collection_index):
	collection_nihr = db['nihr_info']

	_ids_to_index = [rec['_id'] for rec in collection_nihr.find({}, { "_id": 1})]

	for _id in _ids_to_index:
		try:
			rec = collection_nihr.find_one({"_id": _id})
			abstract_text = rec['fields']['plain_english_abstract']
		except KeyError:
			continue
		
		temp_inv_idx = create_index(abstract_text, _id, 'nihr_info')
		update_inverted_index(collection_index, temp_inv_idx)


def index_NLM_text(db, collection_index):
	collection_nlm = db['clinical_trials_NLM_info']

	_ids_to_index = [rec['_id'] for rec in collection_nlm.find({}, { "_id": 1})]

	for _id in _ids_to_index:
		try:
			rec = collection_nlm.find_one({"_id": _id})
			abstract_text = rec['clinical_study']['brief_summary']['textblock']
		except KeyError:
			continue
		
		temp_inv_idx = create_index(abstract_text, _id, 'clinical_trials_NLM_info')
		update_inverted_index(collection_index, temp_inv_idx)

if __name__ == "__main__":
	# Load english stopwords
	english_stopwords = stopwords.words('english')
	
	# Establishing database connection
	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection_index = db['inverted_index']

	collection_index.create_index([('word', pymongo.DESCENDING)], unique=True)
	# # create inverted index on pubmed info
	index_pubmed_text(db, collection_index)
	# # create inverted index on nihrio info
	index_NIHRIO_text(db, collection_index)
	# # create inverted index on nihr info
	index_NIHR_text(db, collection_index)
	# # create inverted index on nlm info
	index_NLM_text(db, collection_index)



	