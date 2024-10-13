from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import JobApplication
from .forms import JobApplicationForm

@login_required
def dashboard(request):
    return render(request, 'job_application/dashboard.html')

@login_required
def job_application_list(request):
    applications = JobApplication.objects.filter(user=request.user)
    return render(request, 'job_application_list.html', {'applications': applications})

@login_required
def job_application_create(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.user = request.user
            job_application.save()
            messages.success(request, 'Job application created successfully.')
            return redirect('job_application_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobApplicationForm()
    return render(request, 'job_application_form.html', {'form': form})

@login_required
def job_application_update(request, pk):
    job_application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job_application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job application updated successfully.')
            return redirect('job_application_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobApplicationForm(instance=job_application)
    return render(request, 'job_application_form.html', {'form': form})

@login_required
def job_application_delete(request, pk):
    job_application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == 'POST':
        job_application.delete()
        messages.success(request, 'Job application deleted successfully.')
        return redirect('job_application_list')
    return render(request, 'job_application_confirm_delete.html', {'job_application': job_application})