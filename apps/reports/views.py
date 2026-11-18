from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import get_reports_data


@login_required
def reports_home(request):
    context = get_reports_data(request.user)
    return render(request, 'reports/reports_home.html', context)
