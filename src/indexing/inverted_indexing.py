import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import json

def create_index(csvreader, file):
	english_stopwords = stopwords.words('english')
	inverted_idx = defaultdict(list)
	
	for row in csvreader:
		word_list = word_tokenize(row[0])
		word_list = [word.lower() for word in word_list if word not in english_stopwords]
		
		pmid = row[-1]

		for word in word_list:
			inverted_idx[word].append(pmid)

		print ("pmid added to inverted index: ", row[-1])

	json.dump(inverted_idx, open(file,'w'))


if __name__ == "__main__":

	csvfile = open('../data/researchfunding.csv', 'r')
	csvreader = csv.reader(csvfile, delimiter = ',')

	create_index(csvreader, '../data/inverted_idx.json')


		




	