from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

# from app.math_proj_helpers import google_rank_rows
from apps.app.csv_helpers import create_csv
from apps.app.ecom_search_helpers import ecom_start_email_search
from apps.app.search_helpers import start_email_search, format_job_titles
from django.contrib.auth.decorators import login_required

from .models import Search, SearchResult, LeadList, Lead

import json
import requests
import datetime

import time
import threading
import queue

# from bs4 import BeautifulSoup
# Create your views here.
def dashboard(request):
    # from django import db
    # print(3)
    # db.connections.close_all()
    if request.user.is_authenticated:
        return render(request, 'app/dashboard.html')
    else:
        return render(request, 'web/landing_page2.html')

@login_required
def get_csv(request, id):
    list = LeadList.objects.get(id=id)
    if request.user.is_staff or list.user == request.user:
        return create_csv(id)
    else:
        return HttpResponse("Unauthorized")

@login_required
def place_search(request):
    if request.method == 'GET':
        return render(request, "app/search.html")
    elif request.method == 'POST':
        num_leads = int(request.POST.__getitem__("num_leads"))
        try:
            num_contacts = int(request.POST.__getitem__("num_contacts"))
        except MultiValueDictKeyError:
            num_contacts = 1

        if num_leads*num_contacts <= request.user.credits:

            request.user.credits -= num_leads*num_contacts
            request.user.save()

            industry = request.POST.__getitem__("industry")
            location = request.POST.__getitem__("location")
            job_titles = request.POST.__getitem__("job_titles")
            try:
                unique_results = (request.POST.__getitem__("unique_results") == "on")
            except MultiValueDictKeyError:
                unique_results = False

            # unique_results = (request.POST.__getitem__("unique_results") == "on")

            job_json = format_job_titles(job_titles)
            print(unique_results)

            #Create the LeadList
            list = LeadList.objects.create(user=request.user, target_num_leads = num_leads, target_num_contacts = num_contacts, job_titles=job_json, unique_results = unique_results)

            if industry == "E-Commerce":
                ecom_start_email_search(list, industry, location, num_leads, num_contacts)
            else:
                start_email_search(list, industry, location, num_leads, num_contacts)
            messages.success(request,f"Began scraping for {industry} leads in {location}.\n\nWe'll email you at {request.user.email} when we've found your results.")
            # return HttpResponseRedirect((reverse("list", args=[list.pk])))
            return HttpResponseRedirect(reverse("lists"))

        else:
            return HttpResponse("Not enough credits")

@login_required
def ecom_search(request):
    if request.method == 'GET':
        return render(request, "app/ecom_search.html")

@login_required
def scrape(request):
    lists = LeadList.objects.filter(user=request.user).order_by('-id')
    src = []
    for list in lists:
        industry = ""
        location = ""
        count = 0
        searches = Search.objects.filter(list=list)
        for search in searches:
            # count += SearchResult.objects.filter(
            #     search=search, valid=True).count()
            # count += SearchResult.objects.filter(
            #     search=search, valid=True).count() - SearchResult.objects.filter(
            #     search=search, valid=True, contact_verified_email = None).count()
            count += Lead.objects.filter(searchResult__search=search).count()
            if (search.industry not in industry):
                industry += search.industry + ", "
            if (search.location not in location):
                location += search.location + ", "
        location = location[:-2]
        industry = industry[:-2]
        src.append({
            'id': list.id,
            'industry': industry,
            'location': location,
            'count': count,
            'status': list.stage
        })
    return render(request, "app/lists.html", {
        'searches': src
    })

@login_required
def list(request, id):
    list = LeadList.objects.get(id=id)
    if request.user.is_staff or list.user == request.user:
        searches = Search.objects.filter(list=list)
        searchResults = []
        count = 0
        for search in searches:
            # count += SearchResult.objects.filter(
            #     search=search, valid=True).count() - SearchResult.objects.filter(
            #     search=search, valid=True, contact_verified_email = None).count()
            count += Lead.objects.filter(searchResult__search=search).count()
        industry = ""
        location = ""
        for search in searches:
            if (search.industry not in industry):
                industry += search.industry + ", "
            if (search.location not in location):
                location += search.location + ", "
            search_res = SearchResult.objects.filter(search=search, valid=True).order_by("id")
            for res in search_res:
                leads = Lead.objects.filter(searchResult=res)
                searchResults.append({"result":res,"leads":leads,"num_leads":len(leads)})
        location = location[:-2]
        industry = industry[:-2]
        # print(searchResults)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            template = "app/table.html"
        else:
            template = "app/list.html"
        if list.job_titles == None:
            job_titles = []
        else:
            job_titles = json.loads(list.job_titles)
        return render(request, template, {
            'job_titles': job_titles,
            'count': count,
            'extra': count-(list.target_num_leads*list.target_num_contacts),
            'target': list.target_num_leads * list.target_num_contacts,
            'leads': list.target_num_leads,
            'contacts': list.target_num_contacts,
            'location': location,
            'industry': industry,
            'searchResults': searchResults,
            'id': id
        })
    else:
        return HttpResponse("Unauthorized")

@login_required
def scrape_status(request, id):
    list = LeadList.objects.get(id=id)
    if request.user.is_staff or list.user == request.user:
        count = 0
        searches = Search.objects.filter(list=list)
        for search in searches:
            # count += SearchResult.objects.filter(
            #     search=search, valid=True).count() - SearchResult.objects.filter(
            #     search=search, valid=True, contact_verified_email = None).count()
            count += Lead.objects.filter(searchResult__search=search).count()
        return JsonResponse({"stage": list.stage,"count": count, "target": list.target_num_leads * list.target_num_contacts}, status=200)
    else:
        return JsonResponse({}, status=400)

@login_required
def num_credits(request):
    return JsonResponse({"credits": request.user.credits}, status=200)

def favicon(request):
    return HttpResponse(4)