import csv
from .models import LeadList, Search, SearchResult
from django.http import HttpResponse

def create_csv(id):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="List '+str(id)+'.csv"'},
    )

    # s = Search.objects.get(id=id)
    # sr = SearchResult.objects.filter(search=s,valid=True)

    list = LeadList.objects.get(id=id)
    searches = Search.objects.filter(list=list)
    sr=[]
    for search in searches:
        search_res = SearchResult.objects.filter(search=search, valid=True)
        for res in search_res:
            sr.append(res)

    fieldnames = ['Searched Industry', 'Searched Location', 'Category', 'Company Website', 'Company Name', 'Company Address', 'Company Phone', 'Company LinkedIn', 'Employee Count', 'Contact Name', 'Contact Title', 'Contact LinkedIn', 'Contact Email', 'Verified']
    writer = csv.DictWriter(response, fieldnames)
    writer.writeheader()
    for search_res in sr:
        writer.writerow({'Searched Industry':search_res.search.industry, 'Searched Location':search_res.search.location, 'Category':search_res.category, 'Company Website':search_res.domain, 'Company Name':search_res.title, 'Company Address':search_res.address, 'Company Phone':search_res.phone, 'Company LinkedIn':search_res.linkedin_url, 'Employee Count':search_res.employee_count, 'Contact Name':search_res.contact_name, 'Contact Title':search_res.contact_title, 'Contact LinkedIn':search_res.contact_linkedin, 'Contact Email':search_res.contact_verified_email, 'Verified':search_res.valid})

    return response