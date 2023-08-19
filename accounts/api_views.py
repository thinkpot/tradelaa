from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from rest_framework.permissions import AllowAny


class TraderAccountCreation(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    http_method_names = ['post', 'patch', 'put']

    # def get_queryset(self):
    #     filters = {}
    #     return self.get_queryset(**filters)