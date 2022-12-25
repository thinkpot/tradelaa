from django.shortcuts import render
from django.views.generic import TemplateView


class DashboardViewSet(TemplateView):
    template_name = 'dashboard/index.html'
