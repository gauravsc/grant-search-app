import requests 


# abstarct to be searched
query = "The purpose of this review is to describe the role of functional renal MRI, or MR renography, in the care of patients with renal masses undergoing partial nephrectomy. MR renography can be used to monitor renal functional outcome for patients undergoing partial nephrectomy and may help guide patient selection in this population with elevated risk of chronic kidney disease."

# top-k of results to be retrieved
topk = 20

# api-endpoint 
URL = "http://127.0.0.1:5000/query/combined_results"
  
# defining a data dict for the post request to be sent to the API 
data = {'query':query, 'topk':topk } 
  
# sending get request and saving the response as response object 
res = requests.post(url = URL, data = data) 
  
# extracting data in json format 
# data = r.json() 

print (res.text)