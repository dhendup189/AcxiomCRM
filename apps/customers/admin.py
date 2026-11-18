
from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'customer_code',
        'customer_name',
        'email',
        'phone',
        'company_name',
        'status',
        'created_date',
    )

    list_filter = ('status', 'state', 'created_date')

    search_fields = (
        'customer_code',
        'customer_name',
        'email',
        'phone',
        'company_name',
    )

    readonly_fields = ('customer_code', 'created_date')

