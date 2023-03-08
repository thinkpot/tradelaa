from rest_framework.viewsets import ViewSet, ModelViewSet
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Trades
from django.db.models import Count
import json
from .serializers import TargetDataSerializer


class TargetHit(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Trades.objects.all()
    serializer_class = TargetDataSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        filters = {'{}'.format(key): value for key, value in query_params.items()}
        return self.queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        print(queryset.annotate(created_count=Count('created_at__date')).values('created_at__date', 'created_count')  )
        new_data = serializer.data
        new_data.insert(0, {
            "count": queryset.count(),
            "x_axis": list(queryset.values_list('created_at', flat=True)),

        })

        return JsonResponse(new_data, safe=False)

