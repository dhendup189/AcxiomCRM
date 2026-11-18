from django.contrib import admin
from .models import FollowUp


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'customer',
        'lead',
        'followup_type',
        'scheduled_at',
        'status',
        'assigned_to',
    )

    list_filter = ('status', 'followup_type', 'scheduled_at')
    search_fields = ('subject', 'notes')
