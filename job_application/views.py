from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'job_application/dashboard.html')
