from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'lead_name',
        'company_name',
        'status',
        'priority',
        'source',
        'assigned_to',
        'created_date',
    )

    list_filter = ('status', 'priority', 'source')
    search_fields = ('lead_name', 'email', 'phone', 'company_name')
