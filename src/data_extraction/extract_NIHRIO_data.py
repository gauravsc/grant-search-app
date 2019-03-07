import pymongo
from pymongo import MongoClient
import csv
import os


# write request size
request_size = 1000

if __name__ == '__main__':
	base_path = '../data/NIHRIO/'

	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection = db['nihrio_info']
	collection.create_index([('id', pymongo.ASCENDING)], unique=True)
	
	files = os.listdir(base_path)
	header = None
	records_to_write = []

	for file in files:
		with open(base_path+file, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=';')
			for row in reader:
				record = {}
				if header is None:
					header = list(row)
					continue
				else:
					for i, val in enumerate(row):
						record[header[i]] = val
					records_to_write.append(record)		

	try:
		collection.insert_many(records_to_write)
	except pymongo.errors.BulkWriteError as e:
		panic = filter(lambda x: x['code'] != 11000, e.details['writeErrors'])
		if len(list(panic)) > 0:
			raise Exception('There was some weird error during insertion that needs to be investigated') 



