from apps.customers.models import Customer
from apps.leads.models import Lead
from apps.followups.models import FollowUp
from apps.opportunities.models import Opportunity
from apps.users.permissions import scope_records


def count_by_choices(queryset, choices, field):
    return [
        {
            'label': label,
            'count': queryset.filter(**{field: value}).count(),
        }
        for value, label in choices
    ]


def get_reports_data(user):
    customers = scope_records(Customer.objects.all(), user, 'customers')
    leads = scope_records(Lead.objects.all(), user, 'leads')
    followups = scope_records(FollowUp.objects.all(), user, 'followups')
    opportunities = scope_records(
        Opportunity.objects.all(), user, 'opportunities'
    )

    active_opportunities = opportunities.exclude(stage__in=['WON', 'LOST'])
    won_opportunities = opportunities.filter(stage='WON')

    pipeline_value = sum((o.amount for o in active_opportunities), 0)
    weighted_pipeline = sum(
        (o.weighted_value for o in active_opportunities), 0
    )
    won_value = sum((o.amount for o in won_opportunities), 0)

    return {
        'customer_total': customers.count(),
        'customer_active': customers.filter(status='ACTIVE').count(),
        'customer_inactive': customers.filter(status='INACTIVE').count(),

        'lead_total': leads.count(),
        'lead_status_report': count_by_choices(
            leads, Lead.STATUS_CHOICES, 'status'
        ),
        'lead_priority_report': count_by_choices(
            leads, Lead.PRIORITY_CHOICES, 'priority'
        ),

        'followup_total': followups.count(),
        'followup_status_report': count_by_choices(
            followups, FollowUp.STATUS_CHOICES, 'status'
        ),

        'opportunity_total': opportunities.count(),
        'opportunity_stage_report': count_by_choices(
            opportunities, Opportunity.STAGE_CHOICES, 'stage'
        ),
        'pipeline_value': pipeline_value,
        'weighted_pipeline': weighted_pipeline,
        'won_value': won_value,
    }