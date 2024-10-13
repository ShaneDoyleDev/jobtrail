from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'job_title', 'job_description_link', 'date_applied', 'date_last_follow_up',
            'recruiter_name', 'recruiter_email', 'hiring_manager_name', 'hiring_manager_email',
            'company_name', 'company_website', 'stage', 'notes', 'cv_sent',
            'cover_letter_sent', 'next_stage_date_time', 'next_stage_prep'
        ]