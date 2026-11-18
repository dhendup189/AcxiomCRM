from django.contrib import admin
from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = (
        'opportunity_name',
        'customer',
        'stage',
        'amount',
        'probability',
        'expected_close_date',
        'assigned_to',
    )

    list_filter = (
        'stage',
        'expected_close_date',
    )

    search_fields = (
        'opportunity_name',
        'customer__customer_name',
    )

    list_editable = (
        'stage',
        'probability',
    )

    ordering = ('-created_date',)
