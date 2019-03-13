import pymongo
from pymongo import MongoClient
import csv
import json

def extract_pubmed_human_studies_data(collection):
	records = collection.find({},{'Abstract':1})

	abstracts = []
	for record in records:
		try:
			abstract = " ".join(record['Abstract'])
			abstracts.append(abstract)
		except KeyError:
			pass

	return abstracts

def extract_NLM_clinical_trials_data(collection):
	records = collection.find({}, {'clinical_study.brief_summary':1})
	
	abstracts = []
	for record in records:
		try:
			abstract = record['clinical_study']['brief_summary']['textblock']
			abstracts.append(abstract)
		except KeyError:
			pass

	return abstracts

def extract_NIHRIO_data(collection):
	records = collection.find({},{'objective':1})

	abstracts = []
	for record in records:
		abstract = record['objective']
		abstracts.append(abstract)

	return abstracts

def extract_NIHR_data(collection):
	records = collection.find({},{'fields.plain_english_abstract':1})

	abstracts = []
	for record in records:
		try:	
			abstract = record['fields']['plain_english_abstract']
			abstracts.append(abstract)
		except KeyError:
			pass

	return abstracts


if __name__ == '__main__':
	# Establishing database connections with different relations
	collection = {}
	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection['pubmed_info'] = db['pubmed_info']
	collection['nihrio_info'] = db['nihrio_info']
	collection['clinical_trials_NLM_info'] = db['clinical_trials_NLM_info']
	collection['nihr_info'] = db['nihr_info'] 

	data = []
	data += extract_pubmed_human_studies_data(collection['pubmed_info'])
	data += extract_NLM_clinical_trials_data(collection['clinical_trials_NLM_info'])
	data += extract_NIHRIO_data(collection['nihrio_info'])
	data += extract_NIHR_data(collection['nihr_info'])


	json.dump(data, open('../processed_data/all_text_abstracts.json', 'w'))






