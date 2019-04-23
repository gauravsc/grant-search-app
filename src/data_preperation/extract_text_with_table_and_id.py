import pymongo
from pymongo import MongoClient
import csv
import json
import csv

def extract_pubmed_human_studies_data(collection, writer):
	records = collection.find({},{'Abstract':1})

	for record in records:
		try:
			abstract = " ".join(record['Abstract'])
			_id = record['_id']
			writer.writerow({'abstract': abstract, '_id':_id, 'table':'pubmed_info'})
		except KeyError:
			pass

	return text_info

def extract_NLM_clinical_trials_data(collection, writer):
	records = collection.find({}, {'clinical_study.brief_summary':1, '_id':1})
	
	for record in records:
		try:
			abstract = record['clinical_study']['brief_summary']['textblock']
			_id = record['_id']
			writer.writerow({'abstract': abstract, '_id':_id, 'table':'clinical_trials_NLM_info'})
		except KeyError:
			pass

	return text_info

def extract_NIHRIO_data(collection, writer):
	records = collection.find({},{'objective':1, '_id':1})

	for record in records:
		abstract = record['objective']
		_id = record['_id']
		writer.writerow({'abstract': abstract, '_id':_id, 'table':'nihrio_info'})

	return text_info

def extract_NIHR_data(collection, writer):
	records = collection.find({},{'fields.plain_english_abstract':1})

	for record in records:
		try:	
			abstract = record['fields']['plain_english_abstract']
			_id = record['_id']
			writer.writerow({'abstract': abstract, '_id':_id, 'table':'nihr_info'})
		except KeyError:
			pass

	return text_info

if __name__ == '__main__':
	# File to save the extracted abstracts
	filename = '../processed_data/all_text_abstracts_mapped_to_table_and_id.csv'
	# Establishing database connections with different relations
	collection = {}
	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection['pubmed_info'] = db['pubmed_info']
	collection['nihrio_info'] = db['nihrio_info']
	collection['clinical_trials_NLM_info'] = db['clinical_trials_NLM_info']
	collection['nihr_info'] = db['nihr_info'] 

	csvfile = open('../processed_data/all_text_abstracts_mapped_to_table_and_id.csv', 'w')
	fieldnames = ['_id', 'table', 'abstract']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	
	extract_pubmed_human_studies_data(collection['pubmed_info'], writer)
	extract_NLM_clinical_trials_data(collection['clinical_trials_NLM_info'], writer)
	extract_NIHRIO_data(collection['nihrio_info'], writer)
	extract_NIHR_data(collection['nihr_info'], writer)


