from django.urls import path
from . import views, api_views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("home/api/v1/", api_views.HomeApiView.as_view(), name="home_api"),
]
