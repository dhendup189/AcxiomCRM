from django.db.models import Sum
from django.utils import timezone

from apps.customers.models import Customer
from apps.leads.models import Lead
from apps.opportunities.models import Opportunity
from apps.users.permissions import scope_records


def get_dashboard_data(user):
    
    customers = Customer.objects.all()
    leads = Lead.objects.all()
    opportunities = Opportunity.objects.all()

   
    customers = scope_records(customers, user, 'customers')
    leads = scope_records(leads, user, 'leads')
    opportunities = scope_records(opportunities, user, 'opportunities')

   
    active_opportunities = opportunities.exclude(
        stage__in=['WON', 'LOST']
    )

   
    open_leads = leads.exclude(
        status__iexact='Converted'
    ).exclude(
        status__iexact='Lost'
    )

    
    won_opportunities = opportunities.filter(stage='WON')

    
    active_pipeline = sum(
        (op.amount for op in active_opportunities),
        0
    )

    weighted_pipeline = sum(
        (op.weighted_value for op in active_opportunities),
        0
    )

    won_sales = sum(
        (op.amount for op in won_opportunities),
        0
    )

   
    lead_status_chart = [
        {
            'label': label,
            'count': leads.filter(status=value).count(),
        }
        for value, label in Lead.STATUS_CHOICES
    ]

    opportunities_by_stage = [
        {
            'label': label,
            'count': opportunities.filter(stage=value).count(),
        }
        for value, label in Opportunity.STAGE_CHOICES
    ]

  
    today = timezone.localdate()

    monthly_sales_chart = []

    for offset in range(5, -1, -1):
        month_number = today.month - offset
        year = today.year

        while month_number <= 0:
            month_number += 12
            year -= 1

        monthly_amount = opportunities.filter(
            stage='WON',
            created_date__year=year,
            created_date__month=month_number,
        ).aggregate(total=Sum('amount'))['total'] or 0

        monthly_sales_chart.append({
            'label': timezone.datetime(year, month_number, 1).strftime('%b'),
            'amount': float(monthly_amount),
        })

    return {
        'total_customers': customers.count(),
        'total_leads': leads.count(),
        'open_leads': open_leads.count(),
        'total_opportunities': opportunities.count(),
        'won_opportunities': won_opportunities.count(),
        'active_pipeline': active_pipeline,
        'weighted_pipeline': weighted_pipeline,
        'won_sales': won_sales,

       
        'recent_customers': customers.order_by('-created_date')[:5],
        'recent_leads': leads.order_by('-created_date')[:5],

        
        'opportunities_by_stage': opportunities_by_stage,

       
        'lead_status_chart': lead_status_chart,
        'opportunity_stage_chart': opportunities_by_stage,
        'monthly_sales_chart': monthly_sales_chart,
    }