from django.contrib import admin
from .models import CustomUser, UserType, OwnBrokers, OwnBrokersCredentials, ZerodhaUsersAccessToken, IsConnectedBroker


admin.site.register(CustomUser)
admin.site.register(UserType)
admin.site.register(OwnBrokers)
admin.site.register(OwnBrokersCredentials)
admin.site.register(ZerodhaUsersAccessToken)
admin.site.register(IsConnectedBroker)
