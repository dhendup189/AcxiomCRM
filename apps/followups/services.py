from django.db.models import Q
from .models import FollowUp


def get_followups(search_query=None, status_filter=None):
    followups = FollowUp.objects.select_related(
        'customer', 'lead', 'assigned_to'
    )

    if search_query:
        followups = followups.filter(
            Q(subject__icontains=search_query) |
            Q(customer__customer_name__icontains=search_query) |
            Q(lead__lead_name__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    if status_filter:
        followups = followups.filter(status=status_filter)

    return followups


def create_followup(cleaned_data, user):
    followup = FollowUp(**cleaned_data)
    followup.created_by = user
    followup.full_clean()
    followup.save()
    return followup


def update_followup(followup, cleaned_data):
    for field, value in cleaned_data.items():
        setattr(followup, field, value)

    followup.full_clean()
    followup.save()
    return followup