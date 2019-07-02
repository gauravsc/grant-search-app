import pymongo
from pymongo import MongoClient
import numpy as np
import random as rd
import os
import json

# global parametes
dim_lsh = 10
path_to_vecs = '../processed_data/vector_representations/'

# set random seed
rd.seed(9001)
np.random.seed(9001)

if __name__ == '__main__':
	# Establishing database connection
	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection_bert_lhs = db['bert_lhs_index']
	collection_bert_lhs.create_index([('bucket', pymongo.TEXT)])

	# generate 25 random vectors
	rand_mat = np.random.standard_normal((dim_lsh, 768))

	# get a list of all the files in the directory
	files = os.listdir(path_to_vecs)
	
	for it, file in enumerate(files):
		print ("Files Done: ", it+1, "/", len(files))
		records = json.load(open(path_to_vecs+file,'r'))
		for record in records:
			vector = np.array(record['representation'])
			original_id = record['_id']
			table = record['table']
			lsh_vec = np.dot(rand_mat, vector)
			lsh_vec[lsh_vec<0] = 0
			lsh_vec[lsh_vec>0] = 1
			lsh_vec = map(str, map(int, lsh_vec))
			bucket = int(''.join(lsh_vec),2)

			# create a document to be inserted into collection
			row = {}
			row['bucket'] = bucket
			row['original_id'] = original_id
			row['table'] = table
			row['vector'] = vector.tolist()

			# insert into the collection
			collection_bert_lhs.insert_one(row)
