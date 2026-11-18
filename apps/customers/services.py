from django.db.models import Q

from .models import Customer


def get_customers(search_query=None):
    """
    Retrieve customers, optionally filtering by a search query.
    """

    customers = Customer.objects.all()

    if search_query:
        customers = customers.filter(
            Q(customer_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(company_name__icontains=search_query)
            | Q(customer_code__icontains=search_query)
        )

    return customers


def create_customer(cleaned_data, user):
    """
    Create a customer and record the user who created it.
    """

    customer = Customer(**cleaned_data)
    customer.created_by = user
    customer.save()

    return customer


def update_customer(customer, cleaned_data):
    """
    Update an existing customer's information.
    """

    for field, value in cleaned_data.items():
        setattr(customer, field, value)

    customer.save()

    return customer


def deactivate_customer(customer):
    """
    Deactivate a customer without permanently deleting its record.
    """

    customer.status = 'INACTIVE'
    customer.save(update_fields=['status'])

    return customer