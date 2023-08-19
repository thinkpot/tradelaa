from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard') ),
    path('tools/', include(('tools.urls', 'tools'), namespace='tools') ),
    path(r'', include(('landingpage.urls', 'landingpage'), namespace='landingpage')),

]
