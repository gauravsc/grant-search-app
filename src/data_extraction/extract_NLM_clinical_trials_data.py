import csv
import time
import urllib
import pickle
import os
import json
import datetime as dt
import pymongo
from pymongo import MongoClient
import xml.etree.ElementTree as ETree
import xmltodict
import json

# Number of rows to be written at once
write_req_size = 1000

def write_to_database(collection, file_paths):
	rows_to_write = []
	for file_path in file_paths:
		record = {}
		with open(file_path, 'r') as f:
			record = f.read()
		record = xmltodict.parse(record)
		rows_to_write.append(record)
		
	try:
		collection.insert_many(rows_to_write)
	except pymongo.errors.BulkWriteError as e:
		panic = filter(lambda x: x['code'] != 11000, e.details['writeErrors'])
		if len(list(panic)) > 0:
			raise Exception('There was some weird error during insertion that needs to be investigated') 

	return True

def get_all_file_paths(base_path):
	folders = os.listdir(base_path)
	folders = [folder for folder in folders if os.path.isdir(base_path+folder)]
	
	all_files_paths = []
	for folder in folders:
		files = os.listdir(base_path+folder)
		for file in files:
			if not file.endswith('.xml'):
				continue
			all_files_paths.append(base_path+folder+'/'+file)	

	return all_files_paths

if __name__ == "__main__":
	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection = db['clinical_trials_NLM_info']
	collection.create_index([('clinical_study.id_info.nct_id', pymongo.ASCENDING)], unique=True)

	base_path = '../data/clinical_trials_NLM_AllPublicXML/'
	all_files_paths = get_all_file_paths(base_path)

	for i in range(0, len(all_files_paths), write_req_size):
		print (f'Files Read: {i}/{len(all_files_paths)}')
		write_to_database(collection, all_files_paths[i:i+write_req_size])

	