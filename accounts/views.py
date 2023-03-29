from django.views.generic import TemplateView
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from rest_framework import status
from django.views.generic.edit import FormView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from rest_framework.views import View
from django.shortcuts import redirect


class SuccessView(TemplateView):
    template_name = 'accounts/success.html'


class SignupView(FormView):
    form_class = SignupForm
    success_url = '/accounts/login/'
    template_name = 'account/signup.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect("/accounts/login/")
        else:
            return JsonResponse({"type": "error"})


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')
    template_name = 'account/login.html'

    def form_valid(self, form):
        credentials = form.cleaned_data
        user = authenticate(username=credentials['email'], password=credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse_lazy('dashboard:dashboard'))

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('login_view'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


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


