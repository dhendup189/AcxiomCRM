from rest_framework import serializers

from apps.customers.models import Customer
from apps.leads.models import Lead
from apps.opportunities.models import Opportunity


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields


class CustomerSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class LeadSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class OpportunitySerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Opportunity
        fields = '__all__'