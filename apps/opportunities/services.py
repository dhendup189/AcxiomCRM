from django.db.models import Q, Sum
from .models import Opportunity


def get_opportunities(search_query=None, stage_filter=None):
    opportunities = Opportunity.objects.select_related(
        'customer',
        'assigned_to'
    )

    if search_query:
        opportunities = opportunities.filter(
            Q(opportunity_name__icontains=search_query) |
            Q(customer__customer_name__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    if stage_filter:
        opportunities = opportunities.filter(stage=stage_filter)

    return opportunities


def create_opportunity(cleaned_data, user):
    opportunity = Opportunity(**cleaned_data)
    opportunity.created_by = user

    opportunity.full_clean()
    opportunity.save()

    return opportunity


def update_opportunity(opportunity, cleaned_data):
    for field, value in cleaned_data.items():
        setattr(opportunity, field, value)

    opportunity.full_clean()
    opportunity.save()

    return opportunity


def get_pipeline_summary():
    opportunities = Opportunity.objects.all()

    active_opportunities = opportunities.exclude(
        stage__in=['WON', 'LOST']
    )

    won_opportunities = opportunities.filter(stage='WON')
    lost_opportunities = opportunities.filter(stage='LOST')

    active_amount = sum(
        (op.amount for op in active_opportunities),
        0
    )

    weighted_pipeline = sum(
        (op.weighted_value for op in active_opportunities),
        0
    )

    won_amount = sum(
        (op.amount for op in won_opportunities),
        0
    )

    return {
        'total_opportunities': opportunities.count(),
        'active_count': active_opportunities.count(),
        'won_count': won_opportunities.count(),
        'lost_count': lost_opportunities.count(),
        'active_amount': active_amount,
        'weighted_pipeline': weighted_pipeline,
        'won_amount': won_amount,
    }