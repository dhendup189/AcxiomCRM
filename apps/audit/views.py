from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import AuditLog
from apps.users.permissions import is_manager_role


@login_required
@user_passes_test(is_manager_role)
def audit_log_list(request):
    logs = AuditLog.objects.select_related('user').all()

    action = request.GET.get('action', '')
    module = request.GET.get('module', '')
    search = request.GET.get('search', '').strip()

    if action:
        logs = logs.filter(action=action)

    if module:
        logs = logs.filter(module=module)

    if search:
        logs = logs.filter(details__icontains=search)

    return render(request, 'audit/audit_list.html', {
        'logs': logs[:500],
        'action_filter': action,
        'module_filter': module,
        'search_query': search,
        'action_choices': AuditLog.ACTION_CHOICES,
    })
