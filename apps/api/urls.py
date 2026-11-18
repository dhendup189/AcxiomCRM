from django.urls import path
from .views import CustomerAPIList, LeadAPIList, OpportunityAPIList

urlpatterns = [
    path('customers/', CustomerAPIList.as_view(), name='api_customers'),
    path('leads/', LeadAPIList.as_view(), name='api_leads'),
    path('opportunities/', OpportunityAPIList.as_view(), name='api_opportunities'),
]