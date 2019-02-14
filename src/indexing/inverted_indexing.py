import pymongo
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import csv
import nltk
import json

# Create inverted index of the words
def create_index(abstract_text, english_stopwords, pmid):
	rows = []
	word_list = word_tokenize(abstract_text)
	word_list = [word.lower() for word in word_list if word not in english_stopwords]
	
	for word in word_list:
		rows.append({"PMID":pmid, "word": word})

	return rows

if __name__ == "__main__":
	# Load english stopwords
	english_stopwords = stopwords.words('english')
	
	# Establishing database connection
	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection_pubmed = db['pubmed_info']
	collection_index = db['pubmed_index']

	pmids = [rec['PMID'] for rec in collection_pubmed.find({}, { "_id": 0, "PMID": 1})]
	pmids_already_indexed = [rec['PMID'] for rec in collection_index.find({},{ "_id": 0, "PMID": 1})]
	pmid_to_index = list(set(pmids).difference(set(pmids_already_indexed)))

	for pmid in pmid_to_index:
		try:
			rec = collection_pubmed.find_one({"PMID": pmid})[0]
		except KeyError:
			continue
		abstract_text = " ".join(rec['Abstract'])
		rows = create_index(abstract_text, english_stopwords, pmid)
		collection_index.insert_many(rows)




	