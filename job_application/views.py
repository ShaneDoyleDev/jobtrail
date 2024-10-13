from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import JobApplicationForm
from .models import JobApplication

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def create_job_application(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.user = request.user
            job_application.save()
        else:
            print(form.errors)
    else:
        form = JobApplicationForm()

    template_name = "create_job_application.html"
    context = {
        "form":form,
    }
    
    return render(request, template_name, context)

