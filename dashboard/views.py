from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import TickerName, TickerTypes, StrikeSideMaster, Trades
from .serializers import TickerNameSerializer, CreateTradeFormSerializer
from django.http import JsonResponse
from .reports import basic_dashboard


class DashboardViewSet(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        data = dict()

        basic_dashboard(data)

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
        print(context['trades'])
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
                return JsonResponse({"msg":"none"})

        filters = {'{}'.format(key): value for key, value in query_params.items()}
        return self.queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
