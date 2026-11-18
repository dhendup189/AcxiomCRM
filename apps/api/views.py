from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import scope_records
from apps.customers.models import Customer
from apps.leads.models import Lead
from apps.opportunities.models import Opportunity

from .serializers import (
    CustomerSerializer,
    LeadSerializer,
    OpportunitySerializer,
)


class CustomerAPIList(ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Customer.objects.all()
        return scope_records(queryset, self.request.user, 'customers')


class LeadAPIList(ListAPIView):
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Lead.objects.all()
        return scope_records(queryset, self.request.user, 'leads')


class OpportunityAPIList(ListAPIView):
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Opportunity.objects.all()
        return scope_records(queryset, self.request.user, 'opportunities')