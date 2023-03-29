from django.contrib import admin
from django.urls import path, include
from .views import HomePageViewSet


urlpatterns = [
    path(r'', HomePageViewSet.as_view(), name='homepage'),
]
