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
from utils.NNSearch import NNSearch
from pytorch_pretrained_bert import BertModel

class RetrieveBertIndex:
	def __init__(self):
		# load pre-trained model tokenizer (vocabulary)
		self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', max_len=512)
		self.max_seq_len = 512
		self.d_word_vec = 200
		self.dropout = 0.1
		self.learning_rate = 0.005

		self.nn_search = NNSearch('../processed_data/vector_representations/')

		print ("Starting to load the saved model .....")
		self.bert = BERTCLassifierModel(dropout=self.dropout)
		# self.model.load_state_dict(torch.load('../saved_models/bert_based/model.pt'))
		# self.bert = BertModel.from_pretrained('bert-base-uncased').cpu()
		# self.bert.load_state_dict(torch.load('../saved_models/bert_based/bert_retrained_mesh_model.pt', map_location='cpu'))
		self.bert.eval()
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

		X = torch.tensor(X, dtype=torch.long)
		Mask = torch.tensor(Mask, dtype=torch.long)
		# print(X.dtype, Mask.dtype)

		encoder_output = self.bert(X, Mask)
		encoder_output = encoder_output.data.numpy()

		return encoder_output[0]

	def retrieve_query_results(self, query, topk=10):
		qu_bert_vec = self.extract_query_vector([query])
		nn_result = self.nn_search.extract_nearest_neighbours(qu_bert_vec, topk=topk)

		return nn_result



		