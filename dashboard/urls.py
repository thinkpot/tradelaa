from django.contrib import admin
from django.urls import path, include
from .views import *
from .micro_apis import SlTpData
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sl-tp-data', SlTpData, basename='sl-tp-data')
router.register(r'create-trade-form', CreateTradeFormViewSet, basename='create-trade-form')

urlpatterns = [
    path(r'', DashboardViewSet.as_view(), name='dashboard'),
    path(r'profile/', UserProfile.as_view(), name='profile'),
    path(r'create-trade/', CreateTrade.as_view(), name='create-analysis'),
    path(r'trade-list', TradesListViewSet.as_view(), name='trades_list'),
    path(r'edit-trade/<str:pk>/', EditTrade.as_view(), name='edit-trade'),
    path(r'r-trade-list', RetailTradesList.as_view(), name='retail-trade-list'),

    #API
    # path(r'create-trade-form/<str:pk>/', CreateTradeFormViewSet.as_view({'post': 'create', 'patch': 'update', 'put': 'update'}), name='create-trade-form'),
    path(r'get-ticker-name/', TickerNameViewSet.as_view({'get': 'list'}), name='get-tickers'),
] + router.urls
