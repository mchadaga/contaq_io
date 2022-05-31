from django.db import models
from contaq_io.settings import AUTH_USER_MODEL
# Create your models here.
# from os import link
# from turtle import title
from django.forms import NullBooleanField

# Create your models here.

class LeadList(models.Model):

    batch_id = models.CharField(max_length=20, null=True)
    stage = models.IntegerField(default=0)
    target_num_leads = models.IntegerField(default=0)
    target_num_contacts = models.IntegerField(default=0)
    job_titles = models.CharField(max_length=300, null=True)
    unique_results = models.BooleanField(default = False)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)

class Search(models.Model):
    industry = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    batch_id = models.CharField(max_length=20, null=True)
    # stage 0 -> Search created 
    # stage 1 -> Companies found
    # stage 2 -> Linkedins & employee names found
    # stage 3 -> Emails Found
    # stage 4 -> Complete
    stage = models.IntegerField(default=0)

    finished_page = models.IntegerField(default=0)
    reached_end = models.BooleanField(default = False)

    list = models.ForeignKey(LeadList, on_delete=models.CASCADE, null=True)


class SearchResult(models.Model):
    rank = models.IntegerField(null=True)
    title = models.CharField(max_length=100, null=True)
    data_id = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    link = models.CharField(max_length=400, null=True)
    domain = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=32, null=True)
    description = models.CharField(max_length=400, null=True)
    snippet = models.CharField(max_length=400, null=True)
    valid = models.BooleanField(default=False)

    linkedin_title = models.CharField(max_length=100, null=True)
    linkedin_url = models.CharField(max_length=200, null=True)

    employee_count = models.IntegerField(null=True)
    employee_order = models.CharField(max_length=2000, null=True)

    contact_name = models.CharField(max_length=200, null=True)
    contact_title = models.CharField(max_length=200, null=True)
    contact_linkedin = models.CharField(max_length=200, null=True)
    contact_verified_email = models.CharField(max_length=200, null=True)

    processed = models.BooleanField(default=False)

    search = models.ForeignKey(Search, on_delete=models.CASCADE)

class Lead(models.Model):

    name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    linkedin = models.CharField(max_length=200, null=True)
    verified_email = models.CharField(max_length=200, null=True)

    searchResult = models.ForeignKey(SearchResult, on_delete=models.CASCADE)