import json
import os
import numpy as np


class NNSearch:
	def __init__(self, path):
		self.path = path

	# small func to compute cosine similarity between two vectors
	def cosine(self, vec1, vec2):
		return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

	# func to maintain a list of topK results sorted by similarity scores
	def add_to_results(self, best_results, cand_triplet, topk):
		if len(best_results) == 0:
			best_results = [cand_triplet]

		elif len(best_results) < topk:
			for i in range(len(best_results)):
				if best_results[i][2] < cand_triplet[2]:
					break
			best_results = best_results[0:i] + [cand_triplet] + best_results[i:]
		else:
			for i in range(len(best_results)):
				if best_results[i][2] < cand_triplet[2]:
					break
				best_results = best_results[0:i] + [cand_triplet] + best_results[i:-1]

		return best_results


	# extract the nearest neighbours using brute force, must be changed later
	def extract_nearest_neighbours(self, query_vector, topk=10):
		query_vector = np.array(query_vector)
		files = os.listdir(self.path); best_results = []
		for file in files[0:1]:
			records = json.load(open(self.path+file,'r'))
			for record in records:
				print (record['table'], record['_id'])
				cand_vector = np.array(record['representation'])
				# # print ("query: ", query_vector[0:10])
				# # print ("candidate vector: ", cand_vector[0:10])
				sim = self.cosine(cand_vector, query_vector)
				cand_triplet = (record['table'], record['_id'], sim)
				best_results = self.add_to_results(best_results, cand_triplet, topk)
		
		return best_results