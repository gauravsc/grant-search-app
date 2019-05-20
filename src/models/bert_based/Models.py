import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from pytorch_pretrained_bert import BertModel

class BERTCLassifierModel(nn.Module):
	def __init__(self, n_tgt_vocab, dropout=0.1):
		super().__init__()
		self.bert = BertModel.from_pretrained('bert-base-uncased')
		self.fc_layer = nn.Linear(768, 768)
		self.output_layer = nn.Linear(768, n_tgt_vocab)


	def forward(self, input_idxs, input_mask):
		enc_out, _ = self.bert(input_idxs, attention_mask=input_mask, output_all_encoded_layers=False)
		# extract encoding for the [CLS] token
		enc_out = enc_out[:,0,:]
		out = self.fc_layer(enc_out)
		# pass the embedding for [CLS] token to the final classification layer
		target = self.output_layer(out)
		
		return target, enc_out
