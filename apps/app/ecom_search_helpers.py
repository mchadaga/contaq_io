from django.http import HttpResponse, HttpResponseRedirect
# from flask import g
# from psycopg2 import Time
import requests
from requests.exceptions import ReadTimeout

from django.core.mail import send_mail
from apps.app.ecom_validate import validate, check_blacklist

import threading
import tldextract

# from urllib3 import Timeout
from .models import LeadList, Search, SearchResult
import datetime
import json
import queue
import time
import math
from django.urls import reverse
import os

from bs4 import BeautifulSoup
import apps.app.search_helpers as search_helpers

def ecom_start_email_search(list, industry, location, count, contacts):

    print("yo")

    #Create the ScaleSERP Batch and fetch its ID
    batch_body = {
        "name": str(datetime.datetime.now())+" Batch",
        "enabled": True,
        "schedule_type": "manual",
        "priority": "normal",
        "searches_type": "mixed"
    }
    batch_result = requests.post(
        'https://api.scaleserp.com/batches?api_key='+os.environ.get("scale_serp_key"), json=batch_body)
    batch_response = batch_result.json()
    id = batch_response['batch']['id']

    list.batch_id = id
    list.save()

    #Create searches
    # locs = location.split(',')
    locs = [location]
    for loc in locs:
        finished_page = 0
        if list.unique_results:
            try:
                finished_page = Search.objects.filter(industry=industry.strip(), location=loc.strip()).order_by("-finished_page")[0].finished_page
            except IndexError:
                finished_page = 0
        s = Search.objects.create(industry=industry.strip(), location=loc.strip(), batch_id=id, list=list, finished_page = finished_page)

    threading.Thread(target=email_search_loop, args=(id, count)).start()

def email_search_loop(id, count):

    list = LeadList.objects.get(batch_id=id)
    searches = Search.objects.filter(list=list)

    emails_found = 0
    while emails_found < count:

        list.stage = 0
        list.save()

        emails_needed = count - emails_found
        num_searches = 1

        # Load Up Searches
        place_searches = []
        for s in searches:
            q = s.location
            for i in range(s.finished_page+1, s.finished_page+1+num_searches):
                if i>4:
                    place_searches.append({
                          'api_key': '311AB9F2410045A69F30606AE563020D',
                            'q': 'buy '+q+' online',
                            'gl': 'us',
                            'hl': 'en',
                            'location': 'United States',
                            'google_domain': 'google.com',
                            'page': str(i-4),
                            'num': '100',
                            'include_answer_box': 'true',
                            'output': 'json',
                            'custom_id': str(s.id)
                    })
                elif i>2:
                    place_searches.append({
                          'api_key': '311AB9F2410045A69F30606AE563020D',
                            'q': q+' store',
                            'gl': 'us',
                            'hl': 'en',
                            'location': 'United States',
                            'google_domain': 'google.com',
                            'page': str(i-2),
                            'num': '100',
                            'include_answer_box': 'true',
                            'output': 'json',
                            'custom_id': str(s.id)
                    })
                else:
                    place_searches.append({
                'api_key': '311AB9F2410045A69F30606AE563020D',
                'q': q,
                'search_type': 'shopping',
                'gl': 'us',
                'hl': 'en',
                'page': str(i),
                'location': 'United States',
                'google_domain': 'google.com',
                'shopping_buy_on_google': 'false',
                'num': '100',
                'shopping_condition': 'new',
                'shopping_filter': 'smb:1',
                'include_html': 'true',
                'output': 'json',
                'custom_id': str(s.id)
                })
            s.finished_page = s.finished_page + num_searches
            s.save()

        # Start Batch
        search_result = requests.put('https://api.scaleserp.com/batches/'+id +
                                    '?api_key=' + os.environ.get("scale_serp_key"), json={'searches': place_searches})

        start_result = requests.get('https://api.scaleserp.com/batches/' +
                                    id+'/start', params={'api_key': os.environ.get("scale_serp_key")})

        num_search_results = fetch_search_results(id, 180)
        print(num_search_results)
        if num_search_results == 0:
            retry_success = False
            if 'search_type' in place_searches[0].keys() and place_searches[0]['search_type']=='shopping':
                for i in range(3):
                    requests.get('https://api.scaleserp.com/batches/' +
                                    id+'/start', params={'api_key': os.environ.get("scale_serp_key")})
                    n_search_results = fetch_search_results(id, 180)
                    if n_search_results != 0:
                        retry_success = True
                        break
            if not retry_success:
                for s in searches:
                    s.reached_end = True
                    s.save()
                break
        search_helpers.remove_duplicates(id)
        print(SearchResult.objects.filter(search__list=list, valid = True, processed=False).count())
        if SearchResult.objects.filter(search__list=list, valid = True, processed=False).count() == 0:
            for s in searches:
                s.reached_end = True
                s.save()
            break
        list.stage = 1
        list.save()
        # search_helpers.linkedin_company_search(id)
        # search_helpers.fetch_linkedin_results(id, 180)
        new_employee_search(id)
        fetch_new_employee_results(id, 180)
        if SearchResult.objects.filter(search__list=list, valid = True, processed=False).count() == 0:
            for s in searches:
                s.reached_end = True
                s.save()
            break
        # search_helpers.linkedin_employee_search(id)
        # search_helpers.fetch_linkedin_employee_results(id, 180)
        # if SearchResult.objects.filter(search__list=list, valid = True, processed=False).count() == 0:
        #     for s in searches:
        #         s.reached_end = True
        #         s.save()
        #     break
        list.stage = 2
        list.save()
        search_helpers.email_search(id, 10)
        list.stage = 3
        list.save()

        emails_found = emails_found + search_helpers.process_results(id)

    print("Completed")
    list.stage = 4
    list.save()

    industry = ""
    location = ""
    for search in searches:
        if (search.industry not in industry):
            industry += search.industry + ", "
        if (search.location not in location):
            location += search.location + ", "
    location = location[:-2]
    industry = industry[:-2]

    if emails_found == 0:
        send_mail(f"We could not find emails of {industry} in {location}",f"We completed your search for {industry} in {location} and unfortunately, no verified emails were found.\n\nPotential reasons for this:\n\n - The chosen industry does not have much online presence: email, website, LinkedIn are required for us to scrape a lead\n - There are few businesses of this industry in your chosen location\n - There are few matches of the job titles you supplied\n\nIf none of these seem likely and you believe there was a technical error, please email support@mg.contaq.io.\n\nEither way, do not worry, your credits for this search have been refunded.\n\nBest,\nContaq.io Team", "Contaq.io Team <support@mg.contaq.io>", [list.user.email])
    else:
        send_mail(f"We found your leads! ({industry} in {location})",f"We completed your search for {industry} in {location} and found {emails_found} verified emails!\n\nTo view your lead list, go to:\n\nhttps://contaq.io/list-{list.id}\n\nTo download the full CSV:\n\nhttps://contaq.io/list-{list.id}/csv\n\nHappy scraping,\nContaq.io Team", "Contaq.io Team <support@mg.contaq.io>", [list.user.email])

    #reimburse credits if necessary
    if emails_found < count:
        list.user.credits += count - emails_found
        list.user.save()

def process_results(batch_id):

    list = LeadList.objects.get(batch_id=batch_id)
    count = 0
    unprocessed_results = SearchResult.objects.filter(search__list = list, processed = False)
    for res in unprocessed_results:
        if res.valid == True:
            count+=1
        res.processed = True
        res.save()

    return count


def fetch_search_results(batch_id, timeout):

    # num_results = 0

    list = LeadList.objects.get(batch_id=batch_id)
    s = Search.objects.filter(list=list)

    def which_search(id):
        for search in s:
            if search.id == id:
                return search
        return None

    dl_response = fetch_next(batch_id, timeout)

    link = dl_response["result"]["download_links"]["pages"][0]
    results = json.loads(requests.get(link).text)

    def sorter(result):
        return result['search']['page']

    res = []

    for r in results:
        res.append(r)

    res.sort(key=sorter)

    # for r in res:
    #     print(r['search']['page'])
    #     if 'places_results' in (r['result'].keys()):
    #         for o in r['result']['places_results']:
    #             if o['sponsored'] == False:
    #                 rank = (r['search']['page']-1)*20+o['position']
    #                 if 'snippet' in o.keys():
    #                     snippet = o['snippet']
    #                 else:
    #                     snippet = None
    #                 if 'link' in o.keys():
    #                     link = o['link']
    #                     domain = link.split("/")[2].replace('www.', '')
    #                 else:
    #                     link = None
    #                     domain = None
    #                 if 'address' in o.keys():
    #                     address = o['address']
    #                 else:
    #                     address = None
    #                 if 'title' in o.keys():
    #                     title = o['title']
    #                 else:
    #                     title = None
    #                 if 'phone' in o.keys():
    #                     phone = o['phone']
    #                 else:
    #                     phone = None
    #                 if 'data_id' in o.keys():
    #                     data_id = o['data_id']
    #                 else:
    #                     data_id = None
    #                 if '$' in o['extensions'][2]:
    #                     category = o['extensions'][3]
    #                 else:
    #                     category = o['extensions'][2]
    #                 SearchResult.objects.create(search=which_search(int(r['search']['custom_id'])), rank=rank, address=address, title=title, phone=phone, data_id=data_id,
    #                                             link=link, domain=domain, category=category, description=snippet, valid=(domain != None), processed=False)
    #                 num_results += 1

    sites = []

    # print(res)

    for r in res:
        #shitty heuristic
        if "search_type" not in r['search'].keys():
            if not r["result"]["search_information"]["original_query_yields_zero_results"] and 'organic_results' in r['result'].keys():
                for o in r['result']['organic_results']:
                    link = o["link"]
                    domain = o["domain"]
                    extracted = tldextract.extract(domain)
                    formatted = "{}.{}".format(extracted.domain,extracted.suffix)
                    if formatted not in sites and validate(link):
                        sites.append(formatted)
        else:
            res_html = r['result']['html']
            # print(res_html)
            soup = BeautifulSoup(res_html, 'lxml')

            product_links = soup.find_all('a', {'class':'LBbJwb shntl'})

            for link in product_links:
                try:
                    site = link['href'].split("/")[5]
                except IndexError:
                    continue
                if site != "product" and site != "products":
                    extracted = tldextract.extract(site)
                    formatted = "{}.{}".format(extracted.domain,extracted.suffix)
                    if formatted not in sites and check_blacklist(site):
                        sites.append(formatted)


    for site in sites:
        SearchResult.objects.create(search=which_search(int(r['search']['custom_id'])), title=site, domain=site, valid=True, processed = False)

    return len(sites)

def remove_duplicates(batch_id):

    list = LeadList.objects.get(batch_id=batch_id)
    # Remove duplicates / bad data
    all_search_results = SearchResult.objects.filter(
        search__list=list, valid=True, processed = False)
    for all_search_res in all_search_results:
        # matches = SearchResult.objects.filter(
        #     search__list=list, valid=True, domain=all_search_res.domain)
        matches = SearchResult.objects.filter(
            search__list=list, domain=all_search_res.domain)
        print(len(matches))
        if len(matches) > 1 and matches[0] != all_search_res:
            all_search_res.valid = False
        elif all_search_res.domain == 'google.com' or all_search_res.domain == 'facebook.com' or all_search_res.domain == 'm.facebook.com':
            all_search_res.valid = False
        all_search_res.save()

    # Stage 1 DONE!
    # linkedin_company_search(batch_id, timeout)


def get_place_details(batch_id):
    list = LeadList.objects.get(batch_id=batch_id)
    if SearchResult.objects.filter(search__list=list, processed=False, domain=None).count() > 2*SearchResult.objects.filter( processed=False,search__list=list).count()//3:
        print("bad links")
        clear_result = requests.delete(
            'https://api.scaleserp.com/batches/'+batch_id+'/clear?api_key='+os.environ.get("scale_serp_key"))
        
        sr = SearchResult.objects.filter(
            search__list=list, processed=False).exclude(data_id=None)

        searches = []

        for search_result in sr:
            search = {
                'search_type': 'place_details',
                'data_id': search_result.data_id,
                'hl': 'en',
                'custom_id': 'P'+str(search_result.id)
            }
            searches.append(search)

        search_res = requests.put('https://api.scaleserp.com/batches/'+batch_id +
                                  '?api_key='+os.environ.get("scale_serp_key"), json={"searches": searches})

        start_result = requests.get('https://api.scaleserp.com/batches/'+batch_id +
                                    '/start', params={'api_key': os.environ.get("scale_serp_key")})

        fetch_place_results(batch_id, 180)

def fetch_next(batch_id, timeout):

    i = 0
    initial = len(requests.get('https://api.scaleserp.com/batches/'+batch_id +
                  '/results', {'api_key': os.environ.get("scale_serp_key")}).json()["results"])

    while i < timeout:
        api_result = requests.get('https://api.scaleserp.com/batches/' +
                                  batch_id+'/results', {'api_key': os.environ.get("scale_serp_key")})
        api_response = api_result.json()
        print(api_response["results"])
        if len(api_response["results"]) > initial:
            break
        time.sleep(1)

    params = {
        'api_key': os.environ.get("scale_serp_key")
    }

    dl_response = requests.get(
        'https://api.scaleserp.com/batches/'+batch_id+'/results/'+str(initial+1), params).json()

    return dl_response


def fetch_place_results(batch_id, timeout):

    dl_response = fetch_next(batch_id, timeout)

    link = dl_response["result"]["download_links"]["pages"][0]
    results = json.loads(requests.get(link).text)

    for r in results:
        custom_id = int(r['search']['custom_id'][1:])
        search_res = SearchResult.objects.get(id=custom_id)
        if not r["result"]["search_information"]["original_query_yields_zero_results"] and "place_details" in r["result"].keys():
            if 'website' in r["result"]["place_details"]:
                search_res.link = r["result"]["place_details"]["website"]
                search_res.domain = r["result"]["place_details"]["website"].split(
                    "/")[2].replace('www.', '')
                search_res.valid = True
            if 'address' in r["result"]["place_details"]:
                search_res.address = r["result"]["place_details"]["address"]
            if 'phone' in r["result"]["place_details"]:
                search_res.phone = r["result"]["place_details"]["phone"]
            search_res.save()


def new_employee_search(batch_id):

    clear_result = requests.delete(
        'https://api.scaleserp.com/batches/'+batch_id+'/clear?api_key='+os.environ.get("scale_serp_key"))
    list = LeadList.objects.get(batch_id=batch_id)
    sr = SearchResult.objects.filter(search__list=list, valid=True, processed=False)

    searches = []

    for search_result in sr:
        domain = search_result.domain
        query = domain+" owner|ceo|founder"

        search = {
            "q": query,
            "location": "United States",
            'gl': 'us',
            'hl': 'en',
            'google_domain': 'google.com',
            'output': 'json',
            'custom_id': str(search_result.id),
            'include_answer_box': 'true'
        }

        searches.append(search)

    # searches_json = {"searches": searches}

    search_res = requests.put('https://api.scaleserp.com/batches/'+batch_id +
                              '?api_key='+os.environ.get("scale_serp_key"), json={"searches": searches})

    start_result = requests.get('https://api.scaleserp.com/batches/'+batch_id +
                                '/start', params={'api_key': os.environ.get("scale_serp_key")})

    # fetch_linkedin_results(batch_id, timeout)


def fetch_new_employee_results(batch_id, timeout):

    num_results = 0

    dl_response = fetch_next(batch_id, timeout)

    link = dl_response["result"]["download_links"]["pages"][0]
    results = json.loads(requests.get(link).text)

    list = LeadList.objects.get(batch_id=batch_id)
    job_titles = json.loads(list.job_titles)

    for r in results:
        # print(r)
        custom_id = int(r['search']['custom_id'])
        # print(custom_id)
        search_res = SearchResult.objects.get(id=custom_id)

        if not r["result"]["search_information"]["original_query_yields_zero_results"] and 'organic_results' in r['result'].keys():
            
            order = []

            for o in r['result']['organic_results']:
                if "linkedin.com/in" in o["link"]:
                    title = o['title'].replace(' – ', ' - ')
                    attributes = title.split(" - ")

                    name = attributes[0]

                    # if search_res.linkedin_title.lower() in name.lower() or len(attributes) < 2:
                    #     continue

                    if len(attributes)>1:
                        job = attributes[1]
                    else:
                        job = ""

                    if 'rich_snippet' in o.keys() and 'top' in o['rich_snippet'].keys() and 'extensions' in o['rich_snippet']['top'].keys() and len(o['rich_snippet']['top']['extensions']) >= 3:
                        job = o['rich_snippet']['top']['extensions'][1]

                    job_lower = job.lower()

                    linkedin = o['link']

                # if 'owner' in job_lower or 'founder' in job_lower or 'chief executive officer' in job_lower or 'ceo' in job_lower or 'head baker' in job_lower or 'chief marketing officer' in job_lower or 'cmo' in job_lower or 'director' in job_lower or ('president' in job_lower and 'vice' not in job_lower):
                #     if 'assistant' in job_lower or len(order) >= 10:
                #         continue
                #     order.append((name, job, linkedin))

                    if 'assistant' in job_lower or len(order) >= 10:
                        continue

                    for job_title in job_titles:
                        if job_title.lower() in job_lower:
                            order.append((name, job, linkedin))
                            break

            
                    # print(search_res.domain+"     "+o["title"])
                    # if 'rich_snippet' in o.keys() and 'top' in o['rich_snippet'].keys() and 'extensions' in o['rich_snippet']['top'].keys():
                    #     print(o['rich_snippet']['top']['extensions'])
                                # name = r['result']['organic_results'][0]['title']
            # try:
            #     new_name = (name[:name.index("| LinkedIn")-1])
            # except:
            #     new_name = name
            # search_res.linkedin_title = new_name
            # search_res.linkedin_url = r['result']['organic_results'][0]['link']
            # search_res.save()
            if order == []:
                search_res.valid = False
            order_json = json.dumps(order)
            search_res.employee_order = order_json
            search_res.save()
        else:
            # search_res.linkedin_title = None
            # search_res.linkedin_url = None
            search_res.valid = False
            search_res.save()

        num_results += 1

    return num_results

    # linkedin_employee_search(batch_id, timeout)


def linkedin_employee_search(batch_id):

    print("hi")

    clear_result = requests.delete(
        'https://api.scaleserp.com/batches/'+batch_id+'/clear?api_key='+os.environ.get("scale_serp_key"))
    list = LeadList.objects.get(batch_id=batch_id)
    # s = Search.objects.get(batch_id=batch_id)
    sr = SearchResult.objects.filter(search__list=list, valid=True, processed=False)

    searches = []

    for search_result in sr:
        name = search_result.linkedin_title
        query = "site:linkedin.com/in intitle:\""+name+"\""

        search = {
            "q": query,
            "location": "United States",
            'gl': 'us',
            'hl': 'en',
            'num': '100',
            'google_domain': 'google.com',
            'output': 'json',
            'custom_id': "E"+str(search_result.id)
        }

        searches.append(search)

    # searches_json = {"searches": searches}

    search_res = requests.put('https://api.scaleserp.com/batches/'+batch_id +
                              '?api_key='+os.environ.get("scale_serp_key"), json={"searches": searches})

    start_result = requests.get('https://api.scaleserp.com/batches/'+batch_id +
                                '/start', params={'api_key': os.environ.get("scale_serp_key")})

    # fetch_linkedin_employee_results(batch_id, timeout)


def fetch_linkedin_employee_results(batch_id, timeout):

    num_results = 0

    dl_response = fetch_next(batch_id, timeout)

    link = dl_response["result"]["download_links"]["pages"][0]
    results = json.loads(requests.get(link).text)

    list = LeadList.objects.get(batch_id=batch_id)
    job_titles = json.loads(list.job_titles)

    for r in results:
        custom_id = int(r['search']['custom_id'][1:])
        search_res = SearchResult.objects.get(id=custom_id)
        if 'organic_results' in r['result'].keys():

            order = []

            for person in r['result']['organic_results']:

                title = person['title'].replace(' – ', ' - ')
                attributes = title.split(" - ")

                name = attributes[0]

                if search_res.linkedin_title.lower() in name.lower() or len(attributes) < 2:
                    continue

                job = attributes[1]

                if 'rich_snippet' in person.keys() and 'top' in person['rich_snippet'].keys() and 'extensions' in person['rich_snippet']['top'].keys() and len(person['rich_snippet']['top']['extensions']) >= 3:
                    job = person['rich_snippet']['top']['extensions'][1]

                job_lower = job.lower()

                linkedin = person['link']

                # if 'owner' in job_lower or 'founder' in job_lower or 'chief executive officer' in job_lower or 'ceo' in job_lower or 'head baker' in job_lower or 'chief marketing officer' in job_lower or 'cmo' in job_lower or 'director' in job_lower or ('president' in job_lower and 'vice' not in job_lower):
                #     if 'assistant' in job_lower or len(order) >= 10:
                #         continue
                #     order.append((name, job, linkedin))

                if 'assistant' in job_lower or len(order) >= 10:
                    continue

                for job_title in job_titles:
                    if job_title.lower() in job_lower:
                        order.append((name, job, linkedin))
                        break

            if order == []:
                search_res.valid = False
            order_json = json.dumps(order)
            search_res.employee_order = order_json
            if 'total_results' in r['result']['search_information'].keys():
                search_res.employee_count = r['result']['search_information']['total_results']
                if r['result']['search_information']['total_results'] > 2000:
                    search_res.valid = False
            else:
                search_res.employee_count = len(r['result']['organic_results'])
            search_res.save()
        else:
            search_res.employee_order = None
            search_res.employee_count = None
            search_res.valid = False
            search_res.save()

        num_results += 1

    return num_results

    # Stage 2 DONE!

    # email_search(batch_id, 10)
    


def email_search(batch_id, workers):

    clear_result = requests.delete(
            'https://api.scaleserp.com/batches/'+batch_id+'/clear?api_key='+os.environ.get("scale_serp_key"))
    
    list = LeadList.objects.get(batch_id=batch_id)
    sr = SearchResult.objects.filter(search__list=list, valid=True, processed=False)

    parameters_queue = queue.Queue()
    # results_queue = queue.Queue(100)

    for search_res in sr:
        print(json.loads(search_res.employee_order))
        try:
            par = (json.loads(search_res.employee_order),
                   search_res.domain, search_res.id)
        except json.decoder.JSONDecodeError:
            par = ([], search_res.domain, search_res.id)
        parameters_queue.put(par)

    # def read_from_queue_and_write_to_db():
    #     while True:
    #         try:
    #             result = results_queue.get(timeout=180)
    #             # result = (id, name, title, linkedin, email)
    #             update_search_res = SearchResult.objects.get(id=result[0])
    #             update_search_res.contact_name = result[1]
    #             update_search_res.contact_title = result[2]
    #             update_search_res.contact_linkedin = result[3]
    #             update_search_res.contact_verified_email = result[4]
    #             if result[4] == None:
    #                 update_search_res.valid = False
    #             # else:
    #             #     emails_found += 1
    #             update_search_res.save()
    #             results_queue.task_done()
    #         except queue.Full:
    #             break

    def find_email(par):
        
        i = 0
        for person in par[0]:

            if i > 10:
                break

            checked = False

            while not checked:

                i += 1

                header = {"x-api-key": os.environ.get("anymail_key")}
                anymail_params = {
                    'full_name': person[0],
                    'domain': par[1]
                }

                try:
                    anymail_request_result = requests.post(
                    'https://api.anymailfinder.com/v4.1/search/person.json', anymail_params, headers=header, timeout = 61)
                except ReadTimeout:
                    return (par[2], None, None, None, None)               

                code = anymail_request_result.status_code
                print(code)

                if code == 429:
                    time.sleep(1)

                if code == 451:
                    return (par[2], None, None, None, None)

                if code == 200:
                    if anymail_request_result.json()['email_class'] == 'verified':

                        email = anymail_request_result.json()['email']
                        neverbounce_request_result = requests.post(
                            "https://api.neverbounce.com/v4/single/check?key="+os.environ.get("neverbounce_key")+"&email="+email)
                        neverbounce_json = neverbounce_request_result.json()
                        if neverbounce_json["result"] == "valid":
                            return (par[2], person[0], person[1], person[2], anymail_request_result.json()['email'])
                        else:
                            return (par[2], None, None, None, None)

                if code != 503 and code != 504 and code != 429 and code != 408:
                    checked = True

        return (par[2], None, None, None, None)

    def query_API_and_write_to_queue():
        while True:
            try:
                par = parameters_queue.get(timeout=5)
                result = find_email(par)
                update_search_res = SearchResult.objects.get(id=result[0])
                update_search_res.contact_name = result[1]
                update_search_res.contact_title = result[2]
                update_search_res.contact_linkedin = result[3]
                update_search_res.contact_verified_email = result[4]
                if result[4] == None:
                    update_search_res.valid = False
                # else:
                #     emails_found += 1
                update_search_res.save()
                parameters_queue.task_done()
            except queue.Empty:
                break

    # db_writer = threading.Thread(target=read_from_queue_and_write_to_db)
    api_readers = [threading.Thread(target=query_API_and_write_to_queue)
                   for i in range(workers)]

    # db_writer.start()
    for ar in api_readers:
        ar.start()

    # wait until thread 1 is completely executed
    # db_writer.join()
    # wait until thread 2 is completely executed
    for ar in api_readers:
        ar.join()

    print("Done!")

def format_job_titles(job_titles):
    titles = job_titles.split("\r\n")
    modified_titles = []
    for title in titles:
        modified_titles.append(title)
        if title == "CEO" and "Chief Executive Officer" not in titles:
            modified_titles.append("Chief Executive Officer")
        elif title == "Chief Executive Officer" and "CEO" not in titles:
            modified_titles.append("CEO")
        elif title == "CMO" and "Chief Marketing Officer" not in titles:
            modified_titles.append("Chief Marketing Officer")
        elif title == "Chief Marketing Officer" and "CMO" not in titles:
            modified_titles.append("CMO")
    return json.dumps(modified_titles)
# def email_search2(batch_id, workers):

#     # emails_found = 0
    
#     list = LeadList.objects.get(batch_id=batch_id)
#     sr = SearchResult.objects.filter(search__list=list, valid=True)

#     parameters_queue = queue.Queue()
#     results_queue = queue.Queue(100)

#     for search_res in sr:
#         print(json.loads(search_res.employee_order))
#         try:
#             par = (json.loads(search_res.employee_order),
#                    search_res.domain, search_res.id)
#         except json.decoder.JSONDecodeError:
#             par = ([], search_res.domain, search_res.id)
#         parameters_queue.put(par)

#     def read_from_queue_and_write_to_db():
#         emails_found = 0
#         while True:
#             try:
#                 result = results_queue.get(timeout=30)
#                 emails_found += 1
#                 print(emails_found)
#                 # result = (id, name, title, linkedin, email)
#                 update_search_res = SearchResult.objects.get(id=result[0])
#                 update_search_res.contact_name = result[1]
#                 update_search_res.contact_title = result[2]
#                 update_search_res.contact_linkedin = result[3]
#                 update_search_res.contact_verified_email = result[4]
#                 if result[4] == None:
#                     update_search_res.valid = False
#                 else:
#                     emails_found += 1
#                 update_search_res.save()
#                 results_queue.task_done()
#             except queue.Full:
#                 break
#             except queue.Empty:
#                 break

#     def find_email(par):
#         return (par[2], None, None, None, None)

#     def query_API_and_write_to_queue():
#         while True:
#             try:
#                 par = parameters_queue.get(timeout=5)
#                 result = find_email(par)
#                 results_queue.put(result)
#                 parameters_queue.task_done()
#             except queue.Empty:
#                 break

#     db_writer = threading.Thread(target=read_from_queue_and_write_to_db)
#     api_readers = [threading.Thread(target=query_API_and_write_to_queue)
#                    for i in range(workers)]

#     db_writer.start()
#     for ar in api_readers:
#         ar.start()

#     # wait until thread 1 is completely executed
#     db_writer.join()
#     # wait until thread 2 is completely executed
#     for ar in api_readers:
#         ar.join()

#     print("Done!")
#     return emails_found

def ecom_search(keyword):
    sites = []

    # set up the request parameters

    for i in range(1,6):
        params = {
            'api_key': '311AB9F2410045A69F30606AE563020D',
            'q': keyword,
            'search_type': 'shopping',
            'gl': 'us',
            'hl': 'en',
            'page': str(i),
            'location': 'United States',
            'google_domain': 'google.com',
            'shopping_buy_on_google': 'false',
            'num': '100',
            'shopping_condition': 'new',
            'include_html': 'true'
            }

        # make the http GET request to Scale SERP
        api_result = requests.get('https://api.scaleserp.com/search', params)

        api_html = api_result.json()['html']

        # print the JSON response from Scale SERP
        soup = BeautifulSoup(api_html, 'lxml')

        product_links = soup.find_all('a', {'class':'LBbJwb shntl'})

        for link in product_links:
            site = link['href'].split("/")[5]
            if site != "product" and site != "products" and site not in sites:
                extracted = tldextract.extract(site)
                formatted = "{}.{}".format(extracted.domain,extracted.suffix)
                sites.append(formatted)

        print(sites)

    return sites
