from django.contrib import admin

from cv.models import CV

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('contact_details',)


# Register the model with the custom admin configuration
admin.site.register(CV, JobApplicationAdmin)
