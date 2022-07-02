import csv
import requests

writefile = open("output.csv", "w")
writer = csv.DictWriter(writefile, fieldnames=["Contact Name", "Contact Title", "Contact LinkedIn", "Company Name", "Location"])
writer.writeheader()

# set up the request parameters
params = {
'api_key': '311AB9F2410045A69F30606AE563020D',
  'q': 'site:linkedin.com/in intitle:"medical planner"',
  'page': '3',
  'num': '100',
  'location': 'United States',
  'hl': 'en',
  'gl': 'us'
}

# make the http GET request to Scale SERP
api_result = requests.get('https://api.scaleserp.com/search', params)

result_json = api_result.json()

for r in result_json["organic_results"]:
    link = r["link"]
    split = r["title"].split("-")
    name = split[0]
    try:
        ext = (r['rich_snippet']['top']['extensions'])
        location = ext[0]
        if len(ext)>1:
            job = ext[1]
        else:
            job = ""
        if len(ext)>2:
            company = ext[2]
        else:
            company = ""
    except KeyError:
        if len(split)>1:
            job = split[1]
        else:
            job = ""
        if len(split)>2:
            company = split[2].split("| LinkedIn")[0]
        else:
            company = ""    
        location = ""
    writer.writerow({"Contact Name":name,"Contact Title":job, "Contact LinkedIn":link, "Company Name":company, "Location":location})
