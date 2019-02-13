from Bio import Entrez
from Bio.Entrez import efetch, read
import csv
import time
import urllib
import pickle
import os 
# Have to define the email id, this is where they contact you in case of excess usage, before blocking you
Entrez.email = 'g.singh@cs.ucl.ac.uk'
# Global variables
request_size = 1000


def fetch_meta_info(pmids):
	pmid_str = ",".join(pmids)
	try:
		handle = efetch(db='pubmed', id=pmid_str, retmode='xml')
	except urllib.error.HTTPError:
		handle = efetch(db='pubmed', id=pmid_str, retmode='xml')

	xml_data = read(handle)['PubmedArticle']	

	try:
		articles = [rec['MedlineCitation'] for rec in xml_data]
	except IndexError:
		articles = None

	return articles


# Convert dates to a string
def date_to_string(date):
	year = date['Year']
	month = date['Month']
	day = date['Day']

	return day+'::'+month+'::'+year


# Extract mesh headings in the form of a list to be saved in the csv file
def extract_mesh_list(raw_mesh_info):
	mesh_list = [str(mesh_info['DescriptorName']).lower() for mesh_info in raw_mesh_info]
	return "::".join(mesh_list)


# Write to file
def write_to_file(pmid_to_write, writer):
	records = fetch_meta_info(pmid_to_write)

	for rec in records:
		row = {}
		try:
			row['PMID'] = str(rec['PMID'])
			row['DateRevised'] = date_to_string(dict(rec['DateRevised']))
			row['DateCompleted'] = date_to_string(dict(rec['DateCompleted']))
			row['MeshHeadingList'] = extract_mesh_list(rec['MeshHeadingList'])
		except KeyError:
			continue
		writer.writerow(row)


def extract_PMID():
	csvfile = open('../data/researchfunding.csv', 'r')
	csvreader = csv.reader(csvfile, delimiter = ',')

	pmid_list = []
	for row in csvreader:
		pmid_list.append(row[-1])

	return pmid_list


if __name__ == '__main__':

	fieldnames = ['PMID', 'MeshHeadingList', 'DateCompleted', 'DateRevised']
	csvfile = open('../data/meta_info_pubmed.csv', 'a')
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	pmid_list = extract_PMID()

	# write all the pertinent content to the file
	if os.path.isfile('../data/meta_info_index.pkl'):
		i = int(pickle.load(open('../data/meta_info_index.pkl','rb')))
	else:
		i = 0

	while i < len(pmid_list):
		pmid_to_write = pmid_list[i:i+request_size]
		write_to_file(pmid_to_write, writer)
		i += request_size
		pickle.dump(i, open('../data/meta_info_index.pkl','wb'))
		time.sleep(5)

