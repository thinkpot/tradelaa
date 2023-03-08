from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LoginView, LogoutView, PasswordResetView
from dashboard.views import DashboardViewSet
from .views import MyProfileView


urlpatterns = [
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout', LogoutView.as_view(), name='account_logout'),
    path('profile/', DashboardViewSet.as_view(), name='dashbaord-view'),
    path('my-profile/', MyProfileView.as_view(), name='my_profile_view')
]
