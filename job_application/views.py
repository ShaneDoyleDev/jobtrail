from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def dashboard(request):
    messages.add_message(request, messages.INFO, "Test messages are working.")
    return render(request, 'job_application/dashboard.html')
