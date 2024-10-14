from django.db import models
from django.contrib.auth import get_user_model 
from colorfield.fields import ColorField
import datetime

User = get_user_model()
# Create your models here.

class Tag(models.Model):
    """Model to represent a Tag."""
    name = models.CharField(max_length=30, unique=True)
    color = ColorField()

    def __str__(self):
        return self.name

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('not_applied', 'Not Applied Yet'),
        ('applied', 'Applied'),
        ('viewed', 'Application Viewed'),
        ('under_review', 'Application Under Review'),
        ('assessment_scheduled', 'Assessment/Test Scheduled'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interview_completed', 'Interview Completed'),
        ('follow_up', 'Follow-Up Required'),
        ('offer_extended', 'Offer Extended'),
        ('offer_accepted', 'Offer Accepted'),
        ('offer_declined', 'Offer Declined'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
        ('hired', 'Hired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length = 30)
    job_link_description = models.URLField(max_length = 200)
    application_posted = models.DateField()
    date_applied = models.DateField(default=datetime.date.today)
    cv = models.FileField(blank=True, null=True)
    cover_letter = models.FileField(blank=True, null=True)
    date_last_followup = models.DateField()
    recruiter_name = models.CharField(max_length= 80)
    recruiter_email = models.EmailField(max_length = 250)
    manager_name = models.CharField(max_length= 80)
    manager_email = models.EmailField(max_length = 250)
    company_name = models.CharField(max_length= 60)
    company_website = models.URLField(max_length = 200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_applied',
    )
    notes = models.TextField()
    next_stage_date_time = models.DateTimeField()
    next_stage_prep = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    salary = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.user})"