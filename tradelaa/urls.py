from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'^accounts/', include('allauth.urls')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard') ),
    path(r'', include(('landingpage.urls', 'landingpage'), namespace='landingpage')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts') )
]
