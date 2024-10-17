from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
# views.py
from django.shortcuts import render, redirect
from .models import CV, ContactDetails, PersonalProfile, EducationItem, HackathonItem, ProjectSkill, Project, Job, SoftSkill
from .forms import (
    ContactDetailsForm, PersonalProfileForm, EducationFormSet, HackathonFormSet,
    ProjectFormSet, JobFormSet, SoftSkillFormSet
)


def generate_pdf(request):
    # Get the template and pass any context data you want to render
    template = get_template('create_pdf.html')
    context = {'name': 'John Doe', 'items': ['Item 1', 'Item 2']}
    html_content = template.render(context)

    # Create a PDF using WeasyPrint
    pdf = HTML(string=html_content).write_pdf()

    # Return the PDF as a downloadable response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response

def create_cv(request):
    # Fetch or create ContactDetails and CV instances for the current user
    contact_details, _ = ContactDetails.objects.get_or_create(user=request.user)
    
    # Check if the user already has a CV
    try:
        cv = CV.objects.get(user=request.user)
    except CV.DoesNotExist:
        cv = None
    
    if request.method == 'POST':
        contact_form = ContactDetailsForm(request.POST, instance=contact_details)
        profile_form = PersonalProfileForm(request.POST, instance=cv.personal_profile if cv else None)

        # Formsets
        education_formset = EducationFormSet(request.POST, prefix='education')
        hackathon_formset = HackathonFormSet(request.POST, prefix='hackathon')
        project_formset = ProjectFormSet(request.POST, prefix='projects')
        job_formset = JobFormSet(request.POST, prefix='jobs')
        soft_skill_formset = SoftSkillFormSet(request.POST, prefix='softskills')

        if contact_form.is_valid() and profile_form.is_valid() and all(
            formset.is_valid() for formset in [
                education_formset, hackathon_formset, project_formset, job_formset, soft_skill_formset
            ]
        ):
            contact_details = contact_form.save(commit=False)
            contact_details.user = request.user
            contact_details.save()

            personal_profile = profile_form.save(commit=False)
            personal_profile.user = request.user
            personal_profile.save()

            # If the CV does not exist, create it
            if not cv:
                cv = CV.objects.create(
                    user=request.user,
                    contact_details=contact_details,
                    personal_profile=personal_profile
                )
            else:
                # Update the existing CV with the new contact details and personal profile
                cv.contact_details = contact_details
                cv.personal_profile = personal_profile
                cv.save()

            # Save ManyToMany fields
            for formset, related_field in zip(
                [education_formset, hackathon_formset, project_formset, job_formset, soft_skill_formset],
                [cv.education_items, cv.hackathon_items, cv.projects, cv.jobs, cv.soft_skills]
            ):
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.user = request.user
                    instance.save()
                    related_field.add(instance)

            return redirect('cv_detail', id=cv.id)
    else:
        # Pre-populate forms and formsets with existing data if available
        contact_form = ContactDetailsForm(instance=contact_details)
        profile_form = PersonalProfileForm(instance=cv.personal_profile if cv else None)
        education_formset = EducationFormSet(queryset=EducationItem.objects.filter(user=request.user), prefix='education')
        hackathon_formset = HackathonFormSet(queryset=HackathonItem.objects.filter(user=request.user), prefix='hackathon')
        project_formset = ProjectFormSet(queryset=Project.objects.filter(user=request.user), prefix='projects')
        job_formset = JobFormSet(queryset=Job.objects.filter(user=request.user), prefix='jobs')
        soft_skill_formset = SoftSkillFormSet(queryset=SoftSkill.objects.filter(user=request.user), prefix='softskills')

    return render(request, 'create_cv.html', {
        'contact_form': contact_form,
        'profile_form': profile_form,
        'education_formset': education_formset,
        'hackathon_formset': hackathon_formset,
        'project_formset': project_formset,
        'job_formset': job_formset,
        'soft_skill_formset': soft_skill_formset,
    })


def cv_detail(request, id):
    cv = get_object_or_404(CV, id=id, user=request.user)  # Ensure the user is authenticated
    return render(request, 'cv_detail.html', {'cv': cv})
