from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^accounts/', include('allauth.urls')),
    path(r'', include('dashboard.urls')),
    path(r'', include('landingpage.urls'))
]
