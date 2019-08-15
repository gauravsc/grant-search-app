from retrieval.retrieval_inverted_index import RetrieveInvertedIndex
from retrieval.retrieval_bert_index import RetrieveBertIndex
import extract_requested_data_for_UI as Data4UI
from flask import Flask, request

app = Flask(__name__)

# creating some global objects
# Retrieve objects using the MeSH trained BERT encoder representations
retr_bert_idx = RetrieveBertIndex()
# Retrieve objects using the inverted index based on words occurence
retr_inv_idx = RetrieveInvertedIndex()

@app.route('/query/bert',  methods='POST')
def retrieve_bert_based_results():
	query = str(request.form["query"])
	topk = int(request.form["topk"])
	# retrieve the query results
	res_bert_idx = retr_bert_idx.retrieve_query_results(query, topk=topk//2)
	output = Data4UI.extract_data(res_bert_idx)
	return output

@app.route('/query/inverted',  methods='POST'):
def retrieve_inverted_index_based_results():
	query = str(request.form["query"])
	topk = int(request.form["topk"])
	# retrieve the query results
	res_inv_idx = retr_inv_idx.retrieve_query_results(query, topk=topk//2)
	output = Data4UI.extract_data(res_inv_idx)
	return output


@app.route('/query/combined_results',  methods='POST')
	query = str(request.form["query"])
	topk = int(request.form["topk"])
	# retrieve the query results from inverted index
	res_inv_idx = retr_inv_idx.retrieve_query_results(query, topk=topk//2)
	# retrieve the query results from bert index
	res_bert_idx = retr_bert_idx.retrieve_query_results(query, topk=topk//2)

	combined_query_results = res_inv_idx + res_bert_idx
	output = Data4UI.extract_data(combined_query_results)

	return output


