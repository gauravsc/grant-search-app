import json
import os
import pickle
import csv
import numpy as np
import random as rd
from nltk.tokenize import word_tokenize
import torch
import torch.nn as nn
import torch.nn.functional as F
from pytorch_pretrained_bert import BertTokenizer
from pytorch_pretrained_bert import BertModel

# Global variables
batch_size = 4
device = 'cuda:0'
max_seq_len = 512

# set random seed
rd.seed(9001)
np.random.seed(9001)

def extract_vector_representations(model, data, tokenizer):
	model = model.eval()
	# fieldnames = ['_id', 'table', 'abstract']
	X = []; Mask = []; 
	for rec in data:
		text = rec['abstract']
		tokenized_text = tokenizer.tokenize('[CLS] ' + text.lower())[0:512]
		idx_seq = tokenizer.convert_tokens_to_ids(tokenized_text)
		src_seq = np.zeros(max_seq_len)
		src_seq[0:len(idx_seq)] = idx_seq
		X.append(src_seq)
		mask = np.zeros(max_seq_len)
		mask[0:len(idx_seq)] = 1
		Mask.append(mask)

	X = np.vstack(X)
	Mask = np.vstack(Mask)

	X = torch.tensor(X).to(device, dtype=torch.long)
	Mask = torch.tensor(Mask).to(device, dtype=torch.long)

	_, encoder_output = model(X, Mask)
	encoder_output = encoder_output.data.to('cpu').numpy()

	records = []
	for idx, row in enumerate(data):
		rec = {}
		rec['table'] = row['table']
		rec['_id'] = row['_id']
		rec['representation'] = encoder_output[idx, :].tolist()
		# print (rec['table'], rec['_id'], row['table'], row['_id'])
		records.append(rec)

	# for i in range(len(records)):
	# 	print ("Records list: ",records[i]['table'], records[i]['_id'])

	return records


if __name__ == '__main__':
	# create  csv dictreader object
	csv_reader = csv.DictReader(open('../processed_data/all_text_abstracts_mapped_to_table_and_id.csv','r'))

	# Load pre-trained model tokenizer (vocabulary)
	tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', max_len=512)

	print ("Starting to load the saved model .....")

	model = BertModel.from_pretrained('bert-base-uncased')
	model.load_state_dict(torch.load('../saved_models/bert_based/bert_retrained_mesh_model.pt'))

	# model.bert.load_state_dict(torch.load('../saved_models/bert_based/bert_retrained_mesh_model.pt'))
	model.to(device)
	print ("Done loading the saved model .....")

	results = []; data = []; ctr = 0;
	for i, row in enumerate(csv_reader):
		# print (i)
		data.append(row)
		if (i+1) % batch_size == 0:
			new_batch_results = extract_vector_representations(model, data, tokenizer)
			results = results + new_batch_results
			data = []
			
			if len(results) % (4*1250) == 0:
				print ("Dumping :", len(results), " results into the file on disk")
				json.dump(results, open('../processed_data/vector_representations/vector_representations_'+str(ctr)+'.json', 'w'))
				results = []; ctr += 1

	if len(results) != 0:
		print ("Dumping :", len(results), " results into the file on disk")
		json.dump(results, open('../processed_data/vector_representations/vector_representations_'+str(ctr)+'.json', 'w'))


