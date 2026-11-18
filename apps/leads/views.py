
from apps.users.permissions import scope_records
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LeadForm
from .models import Lead
from .services import get_leads, create_lead, update_lead


@login_required
def lead_list(request):
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '')

    leads = get_leads(search_query, status_filter)
    leads = scope_records(leads, request.user, 'leads')

    context = {
        'leads': leads,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Lead.STATUS_CHOICES,
    }

    return render(request, 'leads/lead_list.html', context)


@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)

        if form.is_valid():
            create_lead(form.cleaned_data, request.user)
            messages.success(request, 'Lead created successfully.')
            return redirect('lead_list')
    else:
        form = LeadForm()

    return render(request, 'leads/lead_form.html', {
        'form': form,
        'page_title': 'Add Lead'
    })


@login_required
def lead_update(request, lead_id):
    lead_queryset = scope_records(
        Lead.objects.all(), request.user, 'leads'
    )
    lead = get_object_or_404(lead_queryset, id=lead_id)

    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)

        if form.is_valid():
            update_lead(lead, form.cleaned_data)
            messages.success(request, 'Lead updated successfully.')
            return redirect('lead_list')
    else:
        form = LeadForm(instance=lead)

    return render(request, 'leads/lead_form.html', {
        'form': form,
        'page_title': 'Edit Lead'
    })
