from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import get_dashboard_data


@login_required
def dashboard_home(request):
    context = get_dashboard_data(request.user)
    return render(request, 'dashboard/dashboard.html', context)