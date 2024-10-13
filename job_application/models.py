from django.db import models
from django.contrib.auth import get_user_model 
import datetime

User = get_user_model()
# Create your models here.

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length = 30)
    job_link_description = models.URLField(max_length = 200)
    application_posted = models.DateField()
    date_applied = models.DateField(default=datetime.date.today)
    date_last_followup = models.DateField()
    recruiter_name = models.CharField(max_length= 80)
    recruiter_email = models.EmailField(max_length = 250)
    manager_name = models.CharField(max_length= 80)
    manager_email = models.EmailField(max_length = 250)
    company_name = models.CharField(max_length= 60)
    company_website = models.URLField(max_length = 200)
    status = models.CharField(max_length= 20)
    notes = models.TextField()
    next_stage_date_time = models.DateTimeField()
    next_stage_prep = models.TextField()