from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'user',
        'action',
        'module',
        'record_id',
    )
    list_filter = ('action', 'module', 'timestamp')
    search_fields = ('user__username', 'module', 'record_id', 'details')
    readonly_fields = (
        'user',
        'action',
        'module',
        'record_id',
        'details',
        'timestamp',
    )
    ordering = ('-timestamp',)