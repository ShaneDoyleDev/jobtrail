from django.db import models
from django.contrib.auth.models import User

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_description_link = models.URLField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_applied = models.DateField(blank=True, null=True)
    date_last_follow_up = models.DateField(blank=True, null=True)
    recruiter_name = models.CharField(max_length=255, blank=True, null=True)
    recruiter_email = models.EmailField(blank=True, null=True)
    hiring_manager_name = models.CharField(max_length=255, blank=True, null=True)
    hiring_manager_email = models.EmailField(blank=True, null=True)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True, null=True)
    state = models.CharField(max_length=255, choices=[
        ('applied', 'Applied'),
        ('first_round', 'First Round'),
        ('tech_interview', 'Tech Interview'),
    ])
    notes = models.TextField(blank=True, null=True)
    cv_sent = models.URLField(blank=True, null=True, verbose_name='CV Link')
    cover_letter_sent = models.URLField(blank=True, null=True, verbose_name='Cover Letter Link')
    next_stage_date_time = models.DateTimeField(blank=True, null=True)
    next_stage_prep = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    