import csv
import requests

writefile = open("output.csv", "w")
writer = csv.DictWriter(writefile, fieldnames=["Company Name", "Link", "Description"])
writer.writeheader()

params = {
'api_key': '311AB9F2410045A69F30606AE563020D',
  'q': 'buy healthy smoothies online',
  'page': '1',
  'num': '100',
  'location': 'United States',
  'hl': 'en',
  'gl': 'us'
}

api_result = requests.get('https://api.scaleserp.com/search', params)

result_json = api_result.json()

for r in result_json["organic_results"]:
    url = r["link"]
    split_url = url.split("/")
    host = split_url[2]

    slug = split_url[3:]
    if '' in slug:
        slug.remove('')
    if len(slug) == 0:
        name = r["title"]
        desc = r["snippet"]
        writer.writerow({"Company Name":name, "Link":url, "Description":desc})