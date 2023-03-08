from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageViewSet(TemplateView):
    template_name = 'landingpage/landing.html'