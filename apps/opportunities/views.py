from apps.users.permissions import scope_records
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Opportunity
from .forms import OpportunityForm
from .services import (
    get_opportunities,
    create_opportunity,
    update_opportunity,
    get_pipeline_summary,
)


@login_required
def opportunity_list(request):
    search_query = request.GET.get('q', '')
    stage_filter = request.GET.get('stage', '')

    # Filter records based on role
    opportunities = get_opportunities(
        search_query=search_query,
        stage_filter=stage_filter
    )

    opportunities = scope_records(
        opportunities,
        request.user,
        'opportunities'
    )

    # Pipeline totals (we'll scope these as well in the next patch)
    pipeline_summary = get_pipeline_summary()

    context = {
        'opportunities': opportunities,
        'search_query': search_query,
        'stage_filter': stage_filter,
        'stage_choices': Opportunity.STAGE_CHOICES,
        'pipeline_summary': pipeline_summary,
    }

    return render(request, 'opportunities/opportunity_list.html', context)


@login_required
def opportunity_create(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)

        if form.is_valid():
            try:
                create_opportunity(form.cleaned_data, request.user)
                messages.success(request, 'Opportunity created successfully!')
                return redirect('opportunity_list')
            except Exception as e:
                messages.error(request, f'Error creating opportunity: {e}')
    else:
        form = OpportunityForm()

    return render(
        request,
        'opportunities/opportunity_form.html',
        {'form': form, 'title': 'Add Opportunity'}
    )


@login_required
def opportunity_update(request, opportunity_id):
    opportunity_queryset = scope_records(
        Opportunity.objects.all(),
        request.user,
        'opportunities'
    )

    opportunity = get_object_or_404(
        opportunity_queryset,
        id=opportunity_id
    )

    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)

        if form.is_valid():
            try:
                update_opportunity(opportunity, form.cleaned_data)
                messages.success(request, 'Opportunity updated successfully!')
                return redirect('opportunity_list')
            except Exception as e:
                messages.error(request, f'Error updating opportunity: {e}')
    else:
        form = OpportunityForm(instance=opportunity)

    return render(
        request,
        'opportunities/opportunity_form.html',
        {
            'form': form,
            'title': 'Edit Opportunity',
            'opportunity': opportunity
        }
    )