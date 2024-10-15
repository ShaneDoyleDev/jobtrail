from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import mimetypes
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import JobApplicationForm
from .models import JobApplication
from django.utils.dateparse import parse_date
from django.views.generic import ListView
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

class JobApplicationListView(ListView):
    model = JobApplication
    template_name = 'dashboard.html'
    context_object_name = 'job_applications'
    paginate_by = 12

    def get_queryset(self):
        queryset = JobApplication.objects.filter(user=self.request.user)
        
        # Get search query from the GET request
        query = self.request.GET.get('q')
        application_posted_start_date = self.request.GET.get('application_posted_start_date')
        application_posted_end_date = self.request.GET.get('application_posted_end_date')
        
        date_applied_start_date = self.request.GET.get('date_applied_start_date')
        date_applied_end_date = self.request.GET.get('date_applied_end_date')
        
        # Apply text-based filtering
        if query:
            queryset = queryset.filter(
                Q(job_title__icontains=query) |
                Q(recruiter_name__icontains=query) |
                Q(manager_name__icontains=query) |
                Q(company_name__icontains=query) |
                Q(status__icontains=query) |
                Q(notes__icontains=query) |
                Q(next_stage_prep__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        # Apply date range filtering for 'application_posted'
        if application_posted_start_date:
            queryset = queryset.filter(application_posted__gte=parse_date(application_posted_start_date))
        if application_posted_end_date:
            queryset = queryset.filter(application_posted__lte=parse_date(application_posted_end_date))
        # Apply date range filtering for 'application_posted'
        if date_applied_start_date:
            queryset = queryset.filter(date_applied__gte=parse_date(date_applied_start_date))
        if date_applied_end_date:
            queryset = queryset.filter(date_applied__lte=parse_date(date_applied_end_date))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Current date
        today = timezone.now().date()

        # Create a list of dates for the last 14 days
        date_list = [today - timedelta(days=i) for i in range(14)]
        
        # Prepare a dictionary to hold counts for each date initialized to zero
        applications_count = {date.strftime('%m-%d'): 0 for date in date_list}

        # Query for the number of applications for the last 14 days
        applications_last_14_days = (
            JobApplication.objects.filter(date_applied__gte=today - timedelta(days=14))
            .order_by('-date_applied')
            .values('date_applied')
            .annotate(count=Count('id'))
        )

        # Fill in the counts for the corresponding dates
        for application in applications_last_14_days:
            applications_count[application['date_applied'].strftime('%m-%d')] = application['count']

        # Store the count data in the context
        context['applications_last_14_days'] = applications_count
        print(context)

        return context


class JobApplicationDetailView(DetailView):
    model = JobApplication
    template_name = 'detailed_job_application.html'
    context_object_name = 'job_application'


class JobApplicationCreateView(CreateView):
    model = JobApplication
    template_name = 'form_job_application.html'
    form_class = JobApplicationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JobApplicationUpdateView(UpdateView):
    model = JobApplication
    template_name = 'form_job_application.html'
    form_class = JobApplicationForm
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        # Only allow the user to update their own job applications
        return JobApplication.objects.filter(user=self.request.user)


def download_doc(request, doc_type, application_id):
    job_application = get_object_or_404(JobApplication, id=application_id)

    # Open the file in binary mode
    if doc_type == 'cv':
        file = job_application.cv
    elif doc_type == 'cover':
        file = job_application.cover_letter
    file_path = file.path

    # Guess the file's mimetype
    mime_type, _ = mimetypes.guess_type(file_path)

    # Create the HTTP response with the file
    response = HttpResponse(file, content_type=mime_type)

    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = f'attachment; filename={file.name}'

    return response
