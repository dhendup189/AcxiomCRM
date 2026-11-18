
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CRMUserCreationForm
from .permissions import is_admin_role


admin_required = user_passes_test(is_admin_role)


@login_required
@admin_required
def user_list(request):
    users = User.objects.all().order_by('username')

    return render(request, 'users/user_list.html', {
        'users': users,
    })


@login_required
@admin_required
def user_create(request):
    if request.method == 'POST':
        form = CRMUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('crm_user_list')
    else:
        form = CRMUserCreationForm()

    return render(request, 'users/user_form.html', {
        'form': form,
        'page_title': 'Create CRM User',
    })


@login_required
@admin_required
def user_toggle_active(request, user_id):
    if request.method != 'POST':
        return redirect('crm_user_list')

    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        messages.error(request, 'You cannot deactivate your own account.')
        return redirect('crm_user_list')

    target_user.is_active = not target_user.is_active
    target_user.save(update_fields=['is_active'])

    action = 'activated' if target_user.is_active else 'deactivated'
    messages.success(request, f'User {action} successfully.')

    return redirect('crm_user_list')

