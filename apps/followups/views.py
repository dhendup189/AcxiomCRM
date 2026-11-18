
from apps.users.permissions import scope_records
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import FollowUp
from .forms import FollowUpForm
from .services import get_followups, create_followup, update_followup


@login_required
def followup_list(request):
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '')

    followups = get_followups(search_query, status_filter)
    followups = scope_records(followups, request.user, 'followups')

    context = {
        'followups': followups,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': FollowUp.STATUS_CHOICES,
    }

    return render(request, 'followups/followup_list.html', context)


@login_required
def followup_create(request):
    if request.method == 'POST':
        form = FollowUpForm(request.POST)

        if form.is_valid():
            create_followup(form.cleaned_data, request.user)
            messages.success(request, 'Follow-up created successfully.')
            return redirect('followup_list')
    else:
        form = FollowUpForm()

    return render(request, 'followups/followup_form.html', {
        'form': form,
        'page_title': 'Schedule Follow-up'
    })


@login_required
def followup_update(request, followup_id):
    followup_queryset = scope_records(
        FollowUp.objects.all(), request.user, 'followups'
    )
    followup = get_object_or_404(followup_queryset, id=followup_id)

    if request.method == 'POST':
        form = FollowUpForm(request.POST, instance=followup)

        if form.is_valid():
            update_followup(followup, form.cleaned_data)
            messages.success(request, 'Follow-up updated successfully.')
            return redirect('followup_list')
    else:
        form = FollowUpForm(instance=followup)

    return render(request, 'followups/followup_form.html', {
        'form': form,
        'page_title': 'Edit Follow-up'
    })
