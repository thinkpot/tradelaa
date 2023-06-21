from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path(r'option-calculator/', OptionCalculator.as_view(), name='option_calculator'),
    path(r'api/option-calculator/', APIOptionCalculator.as_view(), name='option_cal_api')
]


