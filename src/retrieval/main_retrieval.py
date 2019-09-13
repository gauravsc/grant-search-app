from retrieval.retrieval_inverted_index import RetrieveInvertedIndex
from retrieval.retrieval_bert_index import RetrieveBertIndex

if __name__ == '__main__':
	retr_inv_idx = RetrieveInvertedIndex()
	retr_bert_idx = RetrieveBertIndex()
	query = "The purpose of this review is to describe the role of functional renal MRI, or MR renography, in the care of patients with renal masses undergoing partial nephrectomy. MR renography can be used to monitor renal functional outcome for patients undergoing partial nephrectomy and may help guide patient selection in this population with elevated risk of chronic kidney disease."

	res_inv_idx = retr_inv_idx.retrieve_query_results(query, topk=5)
	res_bert_idx = retr_bert_idx.retrieve_query_results(query, topk=5)

	print ("results of inverted index query: ", res_inv_idx)
	print ("results of bert index query: ", res_bert_idx) 
