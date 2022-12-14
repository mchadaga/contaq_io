from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("local", views.local_dashboard, name="local_dashboard"),
    path("num_credits",views.num_credits,name="num_credits"),
    path("search", views.place_search, name="search"),
    path("exclusions", views.exclusions, name="exclusions"),
    path("ecom_search", views.ecom_search, name="ecom_search"),
    path("lists", views.scrape, name="lists"),
    path("list-<int:id>", views.list, name="list"),
    path('list-<int:id>/csv', views.get_csv, name="get_csv"),
    path('list-<int:id>/status', views.scrape_status, name="scrape_status")
    # path('favicon.ico', views.favicon, name="favicon")
]