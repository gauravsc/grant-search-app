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

def fetch_abstract(pmids):
	pmid_str = ",".join(pmids)
	try:
		handle = efetch(db='pubmed', id=pmid_str, retmode='xml')
	except urllib.error.HTTPError:
		handle = efetch(db='pubmed', id=pmid_str, retmode='xml')

	xml_data = read(handle)['PubmedArticle']	

	try:
		articles = [rec['MedlineCitation']['Article'] for rec in xml_data]
	except IndexError:
		articles = None

	return articles

# function to write the grant data to a file
def write_to_file(pmid_list, categories, fieldnames, writer):
	articles = fetch_abstract(pmid_list)
	
	for i, article_xml in enumerate(articles):
		row = {}
		if article_xml is None or 'Abstract' not in article_xml or 'GrantList' not in article_xml:
			continue

		abstract_info = article_xml['Abstract']['AbstractText']
		abstract_text = " ".join(abstract_info)
		row['Abstract'] = abstract_text

		grant_list = article_xml['GrantList']
		
		grant_ids = []
		grant_agencies = []
		grant_countries = []
		for grant in grant_list:
			if 'GrantID' in grant:
				grant_ids.append(grant['GrantID'])
			else:
				grant_ids.append("")

			if 'Agency' in grant:
				grant_agencies.append(grant['Agency'])
			else:
				grant_agencies.append("")

			if 'Country' in grant:
				grant_countries.append(grant['Country'])
			else:
				grant_countries.append("")

		row['GrantIDs'] = "::".join(grant_ids)
		row['Agencies'] = "::".join(grant_agencies)
		row['Countries'] = "::".join(grant_countries)

		writer.writerow(row)

	return None

if __name__ == "__main__":
	
	categories = {'BACKGROUND':0, 'RESULTS':1,'CONCLUSIONS':2}
	fieldnames = ['Abstract', 'GrantIDs', 'Agencies', 'Countries']
	csvfile = open('../data/researchfunding.csv', 'a')
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


	with open('../data/humanstudypmids.txt', 'r') as f:
		pmid_list = f.readlines()
		pmid_list = [pmid.strip() for pmid in pmid_list]

	# write all the pertinent content to the file
	if os.path.isfile('../data/index.pkl'):
		i = int(pickle.load(open('../data/index.pkl','rb')))
	else:
		i = 0

	while i < len(pmid_list):
		write_to_file(pmid_list[i:i+request_size], categories, fieldnames, writer)
		print ("# docs processed: ", i)
		i += request_size
		pickle.dump(i, open('../data/index.pkl','wb'))
		time.sleep(5)

	# article_xml = fetch_abstract(30526646)
	# abstract_info = article_xml['Abstract']['AbstractText']









