import pymongo
from pymongo import MongoClient
from Bio import Entrez
from Bio.Entrez import efetch, read
import json
import datetime as dt
import csv
import time
import urllib
import pickle
import os 

# Have to define the email id, this is where they contact you in case of excess usage, before blocking you
Entrez.email = 'g.singh@cs.ucl.ac.uk'

# Global variables
request_size = 1000

def fetch_abstract(pmids):
	pmid_str = ",".join(pmids)
	try:
		handle = efetch(db='pubmed', id=pmid_str, retmode='xml')
	except urllib.error.HTTPError:
		handle = efetch(db='pubmed', id=pmid_str, retmode='xml')

	xml_data = read(handle)['PubmedArticle']	

	try:
		articles = [rec['MedlineCitation'] for rec in xml_data]
	except KeyError:
		articles = None

	return articles

# Convert to datetime object
def convert_to_date_object(date_dict):
	date_obj = dt.datetime(int(str(date_dict['Year'])), int(str(date_dict['Month'])), int(str(date_dict['Day'])), 0, 0)
	return date_obj

# Extract mesh headings in the form of a list to be saved in the csv file
def extract_mesh_list(raw_mesh_info):
	mesh_list = [str(mesh_info['DescriptorName']).lower() for mesh_info in raw_mesh_info]
	return mesh_list


def write_to_database(pmids, collection):
	records = fetch_abstract(pmids)
	rows = []
	for rec in records:
		row = {}
		row["PMID"] =  str(rec['PMID'])
		
		try:
			article_xml = rec['Article']
			abstract_info = article_xml['Abstract']['AbstractText']
			row['Abstract'] = abstract_info
		except KeyError:
			pass

		try:
			row['grant'] = article_xml['GrantList']
		except KeyError:
			pass

		try:	
			row['DateRevised'] = convert_to_date_object(dict(rec['DateRevised']))
		except KeyError:
			pass

		try:
			row['DateCompleted'] = convert_to_date_object(dict(rec['DateCompleted']))
		except KeyError:
			pass

		try:	
			row['MeshHeadingList'] = extract_mesh_list(rec['MeshHeadingList'])
		except KeyError:
			pass

		rows.append(row)

	collection.insert_many(rows)


if __name__ == '__main__':
	# Establishing database connection
	client = MongoClient('localhost', 27017)
	db = client['grant_search']
	collection = db['pubmed_info']

	pmids = json.load(open('../data/human_studies_pubmed/human_studies_PMID.json','r'))

	pmids_already_extracted = [rec['PMID'] for rec in collection.find({}, { "_id": 0, "PMID": 1})]

	pmids_to_extract = list(set(pmids).difference(set(pmids_already_extracted)))

	i = 0
	while i < len(pmids_to_extract):
		write_to_database(pmids[i:i+request_size], collection)
		print ("# docs processed: ", i)
		i += request_size
		time.sleep(5)


