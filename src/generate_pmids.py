import csv
import json

def extract_PMID():
	csvfile = open('../data/researchfunding.csv', 'r')
	csvreader = csv.reader(csvfile, delimiter = ',')

	pmid_list = []
	for row in csvreader:
		pmid_list.append(row[-1])


	pmid_list = list(set(pmid_list))
	json.dump(pmid_list, open('../data/human_studies_PMID.json', 'w'))

	return pmid_list

extract_PMID()