import json
import os
import pymongo
from pymongo import MongoClient

if __name__ == '__main__':
	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection = db['nihr_info']
	collection.create_index([('recordid', pymongo.ASCENDING)], unique=True)
	
	base_path = '../data/NIHR_data/'

	files = os.listdir(base_path)

	for file in files:
		data = json.load(open(base_path+file,'r'))

		try:
			collection.insert_many(data)
		except pymongo.errors.BulkWriteError as e:
			panic = filter(lambda x: x['code'] != 11000, e.details['writeErrors'])
			if len(list(panic)) > 0:
				raise Exception('There was some weird error during insertion that needs to be investigated') 

