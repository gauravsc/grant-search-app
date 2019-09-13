import json
import os
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId 


def extract_from_pubmed(collection, query_result):
	record = collection.find_one({'_id':ObjectId(query_result[1])}, {'Abstract':1, 'PMID':1})
	info_to_return = {'PMID':record['PMID'], 'Abstract': " ".join(record['Abstract']), 'Title': 'N/A'}
	return info_to_return

def extract_from_NIHR(collection, query_result):
	record = collection.find_one({'_id':ObjectId(query_result[1])}, {'fields':1})
	info_to_return = {'PMID':'N/A', 'Abstract': record['fields']['plain_english_abstract'], 'Title': record['fields']['project_title']}	
	return info_to_return	

def extract_from_NIHRIO(collection, query_result):
	record = collection.find_one({'_id':ObjectId(query_result[1])})
	info_to_return = {'PMID':'N/A', 'Abstract': record['objective'], 'Title': record['title']}
	return info_to_return

def extract_from_clinical_trials_nlm(collection, query_result):
	record = collection.find_one({'_id':ObjectId(query_result[1])})

	if 'clinical_study' in record and 'official_title' in record['clinical_study']:
		title = record['clinical_study']['official_title']
	else:
		title = "N/A"
	info_to_return = {'PMID':'N/A', 'Abstract': record['clinical_study']['brief_summary']['textblock'], 'Title': title}
	return info_to_return


def extract_data_bert_index(query_results):
	collections = {}
	client = MongoClient('localhost', 27017)
	db = client['grant_search']

	collections['pubmed_info'] = db['pubmed_info']
	collections['nihrio_info'] = db['nihrio_info']
	collections['clinical_trials_NLM_info'] = db['clinical_trials_NLM_info']
	collections['nihr_info'] = db['nihr_info'] 

	extraction_functions = {
	'pubmed_info': extract_from_pubmed,
	'nihrio_info': extract_from_NIHRIO,
	'extract_from_NIHR': extract_from_NIHR,
	'clinical_trials_NLM_info': extract_from_clinical_trials_nlm
	}

	res = []
	for qres in query_results:
		# res += extraction_functions[query_result[0]](collections[query_result[0]], query_result)
		if qres[0] == 'pubmed_info':
			res.append(extract_from_pubmed(collections['pubmed_info'], qres))
		elif qres[0] == 'nihrio_info':
			res.append(extract_from_NIHRIO(collections['nihrio_info'], qres))
		elif qres[0] == 'clinical_trials_NLM_info':
			res.append(extract_from_clinical_trials_nlm(collections['clinical_trials_NLM_info'], qres))
		elif qres[0] == 'nihr_info':
			res.append(extract_from_NIHR(collections['nihr_info'], qres))
	return res


def extract_data_inv_index(query_results):
	collections = {}
	client = MongoClient('localhost', 27017)
	db = client['grant_search']

	collections['pubmed_info'] = db['pubmed_info']
	collections['nihrio_info'] = db['nihrio_info']
	collections['clinical_trials_NLM_info'] = db['clinical_trials_NLM_info']
	collections['nihr_info'] = db['nihr_info'] 

	extraction_functions = {
	'pubmed_info': extract_from_pubmed,
	'nihrio_info': extract_from_NIHRIO,
	'extract_from_NIHR': extract_from_NIHR,
	'clinical_trials_NLM_info': extract_from_clinical_trials_nlm
	}

	res = []
	for qres in query_results:
		qres = (qres[1], str(qres[0]))
		if qres[0] == 'pubmed_info':
			res.append(extract_from_pubmed(collections['pubmed_info'], qres))
		elif qres[0] == 'nihrio_info':
			res.append(extract_from_NIHRIO(collections['nihrio_info'], qres))
		elif qres[0] == 'clinical_trials_NLM_info':
			res.append(extract_from_clinical_trials_nlm(collections['clinical_trials_NLM_info'], qres))
		elif qres[0] == 'nihr_info':
			res.append(extract_from_NIHR(collections['nihr_info'], qres))
	return res


