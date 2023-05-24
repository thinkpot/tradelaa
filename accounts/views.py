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
from fyers_api import accessToken, fyersModel
from django.http import HttpResponse
from django.db import transaction


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
        user = authenticate(email=credentials['email'], password=credentials['password'])
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
        cookie_response.set_cookie('broker', "fyers")

        redirect_response = redirect(reverse_lazy('dashboard:dashboard'))
        redirect_response.set_cookie('access_token', response['access_token'])
        redirect_response.set_cookie('refresh_token', response['refresh_token'])
        redirect_response.set_cookie('broker', "fyers")

        #Checking if already logged in earlier or not
        fyers = fyersModel.FyersModel(client_id=api_key.api_key, token=response['access_token'])
        fyers_respone = fyers.get_profile()

        broker_unique_id = fyers_respone.get('data').get('fy_id')
        # if request.user.is_authenticated:
        #     broker_conn = IsConnectedBroker.objects.filter(user__id=request.user.id, broker_unique_id=broker_unique_id)
        # else:
        broker_conn = IsConnectedBroker.objects.filter(broker_unique_id=broker_unique_id)

        if (not request.user.is_authenticated) and (not broker_conn.exists()):
            with transaction.atomic():
                name_list = fyers_respone.get('data').get('name').split(' ')
                new_user = CustomUser.objects.create(
                    email=fyers_respone.get('data').get('email_id'),
                    phone_number=fyers_respone.get('data').get('mobile_number'),
                    first_name=name_list[0],
                    last_name=name_list[1],
                    user_type=UserType.objects.get(type='RETAIL'),
                    is_active=True
                )
                new_user.set_password(broker_unique_id)
                new_user.save()

                new_user_broker = IsConnectedBroker.objects.create(
                    broker=OwnBrokers.objects.get(short_title='fyers'),
                    broker_unique_id=broker_unique_id,
                    user=new_user
                )
                new_user_broker.save()

            user_auth = authenticate(email=fyers_respone.get('data').get('email_id'), password=fyers_respone.get('data').get('fy_id'))
            login(request, user_auth)

        elif request.user.is_authenticated and (not broker_conn.exists()):
            new_user_broker = IsConnectedBroker.objects.create(
                broker=OwnBrokers.objects.get(short_title='fyers'),
                broker_unique_id=broker_unique_id,
                user=request.user
            )
            new_user_broker.save()

        elif request.user.is_authenticated and broker_conn.exists():
            email = broker_conn.values('user__email').first()
            if request.user.email == email['user__email']:
                return redirect_response
            else:
                return HttpResponse("Already Broker Connect with some account, please try with new account")

        elif (not request.user.is_authenticated) and (broker_conn.exists()):
            email = broker_conn.values('user__email').first()
            user = CustomUser.objects.get(email=email['user__email'])
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect_response
