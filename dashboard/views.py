import datetime

from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import TickerName, TickerTypes, StrikeSideMaster, Trades, UserTrades
from .serializers import TickerNameSerializer, CreateTradeFormSerializer, TradeListAPISerializer, UserTradeDetailsSerializer
from django.http import JsonResponse
from .reports import basic_dashboard
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .helpers import get_fyers_profile, dashboard_decider
from accounts.models import *
from rest_framework.views import APIView
from accounts.models import OwnBrokersCredentials
from fyers_api import fyersModel


class DashboardViewSet(TemplateView):
    template_name = 'dashboard/index.html'

    def dispatch(self, request, *args, **kwargs):
        if (request.COOKIES.get('access_token') == None) and (request.COOKIES.get('logged') != 'True'):
            return redirect(reverse_lazy('accounts:account_login'))
        return super(DashboardViewSet, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        #Retriveing and storing data in context
        context = super().get_context_data()
        data = dict()
        cv = dict()

        basic_dashboard(data)

        if self.request.COOKIES.get('access_token'):
            get_fyers_profile(self.request, data)

        brokers = OwnBrokersCredentials.objects.all()
        cv['brokers'] = brokers

        context['cv'] = cv
        context['data'] = data
        return context


class CreateTrade(TemplateView):
    template_name = 'dashboard/create_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['ticker_types'] = TickerTypes.objects.all()
        context['strike_sides'] = StrikeSideMaster.objects.all()
        return context


class EditTrade(TemplateView):
    template_name = 'dashboard/edit-trade.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        trade = Trades.objects.filter(id=kwargs['pk']).values().first()
        context['trade'] = trade
        context['ticker_types'] = TickerTypes.objects.all()
        context['strike_sides'] = StrikeSideMaster.objects.all()
        print(trade)
        return context


class CreateTradeFormViewSet(ModelViewSet):
    serializer_class = CreateTradeFormSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = Trades.objects.all().order_by('created_at')

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

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


class TradesListViewSet(TemplateView):
    template_name = 'dashboard/trades.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['ticker_types'] = TickerTypes.objects.all()
        context['trades'] = Trades.objects.all().order_by('-created_at')
        context['strike_sides'] = StrikeSideMaster.objects.all()

        return context


class TickerNameViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TickerName.objects.all()
    serializer_class = TickerNameSerializer
    http_method_names = ['get']

    def get_queryset(self):
        query_params = self.request.query_params
        for value in query_params.values():
            if value is None:
                return JsonResponse({"msg": "none"})

        filters = {'{}'.format(key): value for key, value in query_params.items()}
        return self.queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class UserProfile(TemplateView):
    template_name = 'dashboard/account.html'

    def dispatch(self, request, *args, **kwargs):
        if (request.COOKIES.get('access_token') == None) and (request.COOKIES.get('logged') != 'True'):
            return redirect(reverse_lazy('accounts:account_login'))
        return super(UserProfile, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        data = dict()
        if (self.request.COOKIES.get('access_token') != None):
            get_fyers_profile(self.request, data)

        context['data'] = data
        return context


class RetailTradesList(TemplateView):
    template_name = 'dashboard/retail_trades.html'

    def dispatch(self, request, *args, **kwargs):
        if (request.COOKIES.get('access_token') == None) and (request.COOKIES.get('logged') != 'True'):
            return redirect(reverse_lazy('accounts:account_login'))
        return super(RetailTradesList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['ticker_types'] = TickerTypes.objects.all()
        context['trades'] = Trades.objects.filter(trade_date_time__date=datetime.datetime.now().date()).order_by('-created_at')
        context['strike_sides'] = StrikeSideMaster.objects.all()
        return context


class FundsViewSet(TemplateView):
    template_name = 'dashboard/funds.html'

    def dispatch(self, request, *args, **kwargs):
        if (request.COOKIES.get('access_token') == None) and (request.COOKIES.get('logged') != 'True'):
            return redirect(reverse_lazy('accounts:account_login'))
        return super(FundsViewSet, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context


class TradesListAPI(ModelViewSet):
    serializer_class = TradeListAPISerializer
    permission_classes = [AllowAny]
    queryset = Trades.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        query_params = self.request.query_params
        filters = {'{}'.format(key): value for key, value in query_params.items()}
        return self.queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class UserTradeViewSet(ModelViewSet):
    serializer_class = UserTradeDetailsSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserTrades.objects.all()

    def get_queryset(self):
        query_params = self.request.query_params
        filters = {'{}'.format(key): value for key, value in query_params.items()}
        return self.queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({"type": "success", "detail": serializer.data}, safe=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse({"type": "success", "detail": serializer.data}, status=status.HTTP_201_CREATED)


class ExecuteTrade(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        api_key = OwnBrokersCredentials.objects.filter(broker__short_title='fyers').first()
        fyers = fyersModel.FyersModel(client_id=api_key.api_key, token=request.COOKIES.get('access_token'))

        data = self.request.data
        response = fyers.place_order(data=data)
        print(response)

        return JsonResponse({'response': response})