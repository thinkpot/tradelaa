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
from .models import *
from rest_framework.views import APIView
import requests as re
import hashlib
from fyers_api import accessToken
from django.http import HttpResponse


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
            cookie_login = HttpResponseRedirect(reverse_lazy('dashboard:dashboard'))
            cookie_login.set_cookie('logged', True)
            return cookie_login

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('login_view'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        cv = dict()

        brokers = OwnBrokersCredentials.objects.all()
        cv['brokers'] = brokers

        context['cv'] = cv

        return context


class LogoutView(View):
    def post(self, request):
        logout(request)

        broker_logout = redirect("/")
        broker_logout.delete_cookie('access_token')
        broker_logout.delete_cookie('referesh_token')

        return broker_logout


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


class ZerodhaAuthCallback(APIView):
    def get(self, request, *args, **kwargs):
        print(self.request.query_params)

        request_token = self.request.query_params.get('request_token')
        current_user = request.user
        obj, created = ZerodhaUsersAccessToken.objects.update_or_create(user=current_user, request_token=request_token)
        api_key = OwnBrokersCredentials.objects.filter(broker__short_title='zerodha').first()

        zerodha_api_url = 'https://api.kite.trade'
        hash_string = "{0} + {1} + {2}".format(api_key.api_key, request_token, api_key.api_key)
        hash_string = hash_string.encode('utf-8')
        print(hash_string)
        request_hash = hashlib.sha256(hash_string).hexdigest()
        request_payload = {
            "request_token": request_token,
            "checksum": request_hash,
            "api_key": api_key.api_key
        }
        print(request_hash)
        response = re.post(url=zerodha_api_url+'/session/token', data=request_payload)
        print(response.json())
        return JsonResponse(response.json())


class FyersAuthCallback(APIView):
    def get(self, request, *args, **kwargs):

        auth_code = self.request.query_params.get('auth_code')
        obj, created = FyersUsersAccessToken.objects.update_or_create(auth_code=auth_code)
        api_key = OwnBrokersCredentials.objects.filter(broker__short_title='fyers').first()


        session = accessToken.SessionModel(
            client_id=api_key.api_key,
            secret_key=api_key.api_secret,
            response_type='code',
            grant_type='authorization_code',
        )
        session.set_token(auth_code)
        response = session.generate_token()

        cookie_response = JsonResponse(response, safe=False)
        cookie_response.set_cookie('access_token', response['access_token'])
        cookie_response.set_cookie('refresh_token', response['refresh_token'])

        redirect_response = redirect(reverse_lazy('dashboard:dashboard'))
        redirect_response.set_cookie('access_token', response['access_token'])
        redirect_response.set_cookie('refresh_token', response['refresh_token'])

        return redirect_response
