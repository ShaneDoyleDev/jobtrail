from django.contrib import admin
from .models import Tag, JobApplication

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'user', 'status')
    filter_horizontal = ('tags',)  # Allows easier management of many-to-many relationships


# Register the model with the custom admin configuration
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(Tag, TagAdmin)