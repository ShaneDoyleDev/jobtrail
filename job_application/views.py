from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import mimetypes

from .forms import JobApplicationForm
from .models import JobApplication

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def create_job_application(request):
    if request.method == "POST":
        print(request.FILES)
        form = JobApplicationForm(request.POST, request.FILES)

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

def download_doc(request, doc_type, application_id):
    job_application = get_object_or_404(JobApplication, id=application_id)

    # Open the file in binary mode
    if doc_type == 'cv':
        file = job_application.cv
    else:
        file = job_application.cover_letter
    file_path = file.path

    # Guess the file's mimetype
    mime_type, _ = mimetypes.guess_type(file_path)

    # Create the HTTP response with the file
    response = HttpResponse(file, content_type=mime_type)
    
    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = f'attachment; filename={file.name}'

    return response

@login_required
def detailed__job_application(request, id):
    job_application = JobApplication.objects.get(user=request.user, id=id)
    
    return render(request, 'detailed_job_application.html', {'job_application': job_application})