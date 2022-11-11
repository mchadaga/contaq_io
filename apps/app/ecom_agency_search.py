import csv
import requests
import os

writefile = open("output.csv", "w")
writer = csv.DictWriter(writefile, fieldnames=["Company Name", "Company LinkedIn", "Description"])
writer.writeheader()

params = {
'api_key': os.environ.get("scale_serp_key"),
  'q': 'site:https://www.linkedin.com/company ("ecommerce"|"ecom") +"agency" +"View all 2"',
  'page': '4',
  'num': '100',
  'location': 'United States',
  'hl': 'en',
  'gl': 'us'
}

api_result = requests.get('https://api.scaleserp.com/search', params)

result_json = api_result.json()

for r in result_json["organic_results"]:
    name = r["title"].split("LinkedIn")[0]
    url = r["link"]
    desc = r["snippet"]
    writer.writerow({"Company Name":name, "Company LinkedIn":url, "Description":desc})
