
from apps.users.permissions import scope_records
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomerForm
from .models import Customer
from .services import (
    create_customer,
    deactivate_customer,
    get_customers,
    update_customer,
)


@login_required
def customer_list(request):
    search_query = request.GET.get('search', '').strip()

    customers = get_customers(search_query)
    customers = scope_records(customers, request.user, 'customers')

    context = {
        'customers': customers,
        'search_query': search_query,
    }

    return render(request, 'customers/customer_list.html', context)


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            create_customer(form.cleaned_data, request.user)
            messages.success(request, 'Customer created successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'customers/customer_form.html', {
        'form': form,
        'page_title': 'Add Customer',
    })


@login_required
def customer_update(request, customer_id):
    customer_queryset = scope_records(
        Customer.objects.all(), request.user, 'customers'
    )
    customer = get_object_or_404(customer_queryset, id=customer_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            update_customer(customer, form.cleaned_data)
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_form.html', {
        'form': form,
        'page_title': 'Edit Customer',
    })


@login_required
def customer_deactivate(request, customer_id):
    if request.method != 'POST':
        messages.warning(request, 'Invalid request.')
        return redirect('customer_list')

    customer_queryset = scope_records(
        Customer.objects.all(), request.user, 'customers'
    )
    customer = get_object_or_404(customer_queryset, id=customer_id)

    deactivate_customer(customer)
    messages.success(request, 'Customer deactivated successfully.')

    return redirect('customer_list')
