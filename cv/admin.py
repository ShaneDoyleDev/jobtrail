from django.contrib import admin
from .models import (
    ContactDetails,
    PersonalProfile,
    EducationItem,
    HackathonItem,
    TechnicalSkill,
    Project,
    Job,
    JobBulletPoint,
    SoftSkill,
    CV,
)

# Define an admin class for each model if you want to customize the admin interface

class ContactDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'phone_number')
    search_fields = ('name', 'email')
    list_filter = ('user',)

class PersonalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'description')
    search_fields = ('user__username',)

class EducationItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'start_year', 'end_year', 'area_of_study', 'result')
    search_fields = ('school', 'area_of_study')
    list_filter = ('user', 'start_year', 'end_year')

class HackathonItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition_name', 'year_month', 'hosts')
    search_fields = ('competition_name', 'hosts')
    list_filter = ('user', 'year_month')

class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill')
    search_fields = ('skill',)
    list_filter = ('user',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_name', 'description')
    search_fields = ('project_name', 'description')
    list_filter = ('user',)

class JobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'company', 'start_date', 'end_date')
    search_fields = ('job_title', 'company')
    list_filter = ('user', 'start_date', 'end_date')

class JobBulletPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'jbp')
    search_fields = ('jbp',)
    list_filter = ('user', 'job')

class SoftSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'group_name')
    search_fields = ('group_name',)
    list_filter = ('user',)

class CVAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_details', 'personal_profile')
    search_fields = ('user__username',)
    list_filter = ('user',)

# Register the models with the admin site
admin.site.register(ContactDetails, ContactDetailsAdmin)
admin.site.register(PersonalProfile, PersonalProfileAdmin)
admin.site.register(EducationItem, EducationItemAdmin)
admin.site.register(HackathonItem, HackathonItemAdmin)
admin.site.register(TechnicalSkill, TechnicalSkillAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobBulletPoint, JobBulletPointAdmin)
admin.site.register(SoftSkill, SoftSkillAdmin)
admin.site.register(CV, CVAdmin)

