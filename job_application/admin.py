from django.contrib import admin
from job_application.models import JobApplication

# Register your models here.
class JobApplicationAdmin(admin.ModelAdmin):
    pass

# Register the model with the custom admin configuration
admin.site.register(JobApplication, JobApplicationAdmin)