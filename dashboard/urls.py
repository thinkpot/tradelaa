from django.contrib import admin
from django.urls import path, include
from .views import DashboardViewSet


urlpatterns = [
    path(r'dashboard/', DashboardViewSet.as_view(), name='dashboard'),
]
