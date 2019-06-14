import json
import pymongo
import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from pymongo import MongoClient
from pytorch_pretrained_bert import BertTokenizer
from models.bert_based.Models import BERTCLassifierModel

class RetrieveBertIndex:
	def __init__(self):
		# load pre-trained model tokenizer (vocabulary)
		self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', max_len=512)

		# # create the vocabulary of mesh terms
		# with open('../data/mesh_to_idx.pkl', 'rb') as fread:
		# 	mesh_to_idx = pickle.load(fread)
		
		# mesh_vocab = [" "] * len(mesh_to_idx)
		# for mesh, idx in mesh_to_idx.items():
		# 	mesh_vocab[idx] = mesh

		# setting model parameters
		self.n_tgt_vocab = len(mesh_to_idx)
		self.max_seq_len = 512
		self.d_word_vec = 200
		self.dropout = 0.1
		self.learning_rate = 0.005

		print ("Starting to load the saved model .....")
		self.model = BERTCLassifierModel(self.n_tgt_vocab, dropout=self.dropout)
		self.model.load_state_dict(torch.load('../saved_models/bert_based/model.pt'))
		self.model.eval()
		print ("Done loading the saved model .....")


	def extract_query_vector(self, queries):
		X = []; Mask = []; 
		for query in queries:
			tokenized_text = self.tokenizer.tokenize('[CLS] ' + query.lower())[0:512]
			idx_seq = self.tokenizer.convert_tokens_to_ids(tokenized_text)
			src_seq = np.zeros(self.max_seq_len)
			src_seq[0:len(idx_seq)] = idx_seq
			X.append(src_seq)
			mask = np.zeros(self.max_seq_len)
			mask[0:len(idx_seq)] = 1
			Mask.append(mask)

		X = np.vstack(X)
		Mask = np.vstack(Mask)

		X = torch.tensor(X)
		Mask = torch.tensor(Mask)

		_, encoder_output = model(X, Mask)
		encoder_output = encoder_output.data.numpy()

		return encoder_output[0]


	def extract_nearest_neighbours(self, bert_vector, path):
		files = os.listdir(path); best_results = []
		for file in files:
			records = json.load(open(path+file,'r'))
			for record in records:
						



	def retrieve_query_results(self, query, topk=10):
		path = '../processed_data/vector_representations/'
		qu_bert_vec = self.extract_bert_vector([query])
		nn_result = self.extract_nearest_neighbours(qu_bert_vec, path)



		