"""URL routes for the server-rendered frontend pages."""
from django.urls import path

from . import web_views

urlpatterns = [
    path("", web_views.campaign_list, name="campaign_list"),
    path("campaigns/<int:pk>/", web_views.campaign_detail, name="campaign_detail"),
    path("campaigns/<int:pk>/donate/", web_views.donate, name="donate"),
]
