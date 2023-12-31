from django.contrib import admin
from django.urls import path, include
from dashboard.views import DashboardViewSet
from .views import *
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .api_views import TraderAccountCreation
from rest_framework import routers

router = routers.DefaultRouter()
router.register('create-trader-account', TraderAccountCreation, basename='create-traders')

urlpatterns = [
    path(r'success/', SuccessView.as_view(), name="success_view"),
    path(r'signup/', SignupView.as_view(), name="account_signup"),
    path(r'login/', LoginView.as_view(), name='account_login'),
    path(r'logout/', LogoutView.as_view(), name='account_logout'),
    path(r'zerodha-auth/', ZerodhaAuthCallback.as_view(), name='zerodha_auth'),
    path(r'fyers-auth/', FyersAuthCallback.as_view(), name='fyers_auth'),
    #------------------------Accounts APIS---------------------------

]