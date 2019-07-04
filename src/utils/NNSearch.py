import json
import os
import random as rd
import numpy as np
import pymongo
from pymongo import MongoClient

# set global params
dim_lsh = 6

# set random seed
rd.seed(9001)
np.random.seed(9001)

class NNSearch:
	def __init__(self, path):
		# Establishing database connection
		client = MongoClient('localhost', 27017)
		db = client['grant_search']
		self.collection_bert_lhs = db['bert_lhs_index']
		
		# generate 25 random vectors
		self.rand_mat = np.random.standard_normal((dim_lsh, 768))

	# small func to compute cosine similarity between two vectors
	def cosine(self, vec1, vec2):
		return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

	# extract the top-k records based on cosine similarity score	
	def extract_nearest_neighbours(self, query_vector, topk=10):
		query_vector = np.array(query_vector)

		# estimate which bucket the document will fall into
		lsh_vec = np.dot(self.rand_mat, query_vector)
		lsh_vec[lsh_vec<0] = 0
		lsh_vec[lsh_vec>0] = 1
		lsh_vec = map(str, map(int, lsh_vec))
		bucket = int(''.join(lsh_vec),2)

		# retrieve all the documents that are in the same bucket
		records = self.collection_bert_lhs.find({"bucket": bucket})

		top_results = []
		for record in records:
			# print (record['vector'])
			cand_vector = np.array(record['vector'])
			sim = self.cosine(cand_vector, query_vector)
			cand_triplet = (record['table'], record['original_id'], sim)

			# put the record in the right position
			if len(top_results) == 0:
				top_results = [cand_triplet]

			elif len(top_results) < topk:
				for i in range(len(top_results)):
					if top_results[i][2] < cand_triplet[2]:
						break
				top_results = top_results[0:i] + [cand_triplet] + top_results[i:]
			else:
				for i in range(len(top_results)):
					if top_results[i][2] < cand_triplet[2]:
						break
				top_results = top_results[0:i] + [cand_triplet] + top_results[i:-1]
			
		return top_results