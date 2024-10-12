from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def dashboard(request):
    messages.success(request, "Test messages are working.")
    return render(request, 'job_application/dashboard.html')
