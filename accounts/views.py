from django.shortcuts import render
from django.views.generic import TemplateView
from allauth.account.views import PasswordResetView, PasswordChangeView
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from rest_framework import status


class ProfileViewSet(TemplateView):
    template_name = 'dashboard/index.html'


class PasswordResetViewSet(PasswordResetView):
    template_name = ''


class MyProfileView(TemplateView):
    template_name = 'dashboard/account.html'


class MyProfileAPI(ModelViewSet):
    http_method_names = ["patch", "put"]

    def get_queryset(self):
        query_params = self.request.query_params
        filters = {'{}'.format(key): value for key, value in query_params.items()}
        return self.queryset.filter(**filters)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


