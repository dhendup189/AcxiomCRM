from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

   
    path('accounts/', include('django.contrib.auth.urls')),

    path('', include('apps.dashboard.urls')),
   
    path('customers/', include('apps.customers.urls')),
    path('leads/', include('apps.leads.urls')),
    path('followups/', include('apps.followups.urls')),
    path('opportunities/', include('apps.opportunities.urls')),
    path('users/', include('apps.users.urls')),
    path('audit/', include('apps.audit.urls')),
    path('api/', include('apps.api.urls')),
    path('reports/', include('apps.reports.urls')),
]
