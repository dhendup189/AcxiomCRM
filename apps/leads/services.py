from django.db.models import Q
from .models import Lead


def get_leads(search_query=None, status_filter=None):
    leads = Lead.objects.select_related('assigned_to', 'created_by')

    if search_query:
        leads = leads.filter(
            Q(lead_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(company_name__icontains=search_query)
        )

    if status_filter:
        leads = leads.filter(status=status_filter)

    return leads


def create_lead(cleaned_data, user):
    lead = Lead(**cleaned_data)
    lead.created_by = user
    lead.save()
    return lead


def update_lead(lead, cleaned_data):
    for field, value in cleaned_data.items():
        setattr(lead, field, value)
    lead.save()
    return lead