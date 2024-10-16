from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
# views.py
from django.shortcuts import render, redirect
from .models import CV, ContactDetails, PersonalProfile, EducationItem, HackathonItem, TechnicalSkill, Project, Job, SoftSkill
from .forms import (
    ContactDetailsForm, PersonalProfileForm, EducationFormSet, HackathonFormSet,
    TechnicalSkillFormSet, ProjectFormSet, JobFormSet, SoftSkillFormSet
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
    contact_details, created = ContactDetails.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        
        contact_form = ContactDetailsForm(request.POST, instance=contact_details)
        profile_form = PersonalProfileForm(request.POST)

        # Formsets
        education_formset = EducationFormSet(request.POST, prefix='education')
        hackathon_formset = HackathonFormSet(request.POST, prefix='hackathon')
        skill_formset = TechnicalSkillFormSet(request.POST, prefix='skills')
        project_formset = ProjectFormSet(request.POST, prefix='projects')
        job_formset = JobFormSet(request.POST, prefix='jobs')
        soft_skill_formset = SoftSkillFormSet(request.POST, prefix='softskills')

        if contact_form.is_valid() and profile_form.is_valid() and all(
            [education_formset.is_valid(), hackathon_formset.is_valid(), skill_formset.is_valid(),
             project_formset.is_valid(), job_formset.is_valid(), soft_skill_formset.is_valid()]
        ):
            contact_details = contact_form.save(commit=False)
            contact_details.user = request.user
            contact_details.save()

            personal_profile = profile_form.save(commit=False)
            personal_profile.user = request.user
            personal_profile.save()

            # Create the CV instance
            cv = CV.objects.create(
                user=request.user,
                contact_details=contact_details,
                personal_profile=personal_profile
            )

            # Save ManyToMany fields
            for formset, related_field in zip(
                [education_formset, hackathon_formset, skill_formset, project_formset, job_formset, soft_skill_formset],
                [cv.education_items, cv.hackathon_items, cv.technical_skills, cv.projects, cv.jobs, cv.soft_skills]
            ):
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.user = request.user
                    instance.save()
                    related_field.add(instance)

            return redirect('cv_detail', pk=cv.pk)

    else:
        # Initialize empty forms and formsets
        contact_form = ContactDetailsForm(instance=contact_details)
        profile_form = PersonalProfileForm()
        education_formset = EducationFormSet(queryset=EducationItem.objects.none(), prefix='education')
        hackathon_formset = HackathonFormSet(queryset=HackathonItem.objects.none(), prefix='hackathon')
        skill_formset = TechnicalSkillFormSet(queryset=TechnicalSkill.objects.none(), prefix='skills')
        project_formset = ProjectFormSet(queryset=Project.objects.none(), prefix='projects')
        job_formset = JobFormSet(queryset=Job.objects.none(), prefix='jobs')
        soft_skill_formset = SoftSkillFormSet(queryset=SoftSkill.objects.none(), prefix='softskills')

    return render(request, 'create_cv.html', {
        'contact_form': contact_form,
        'profile_form': profile_form,
        'education_formset': education_formset,
        'hackathon_formset': hackathon_formset,
        'skill_formset': skill_formset,
        'project_formset': project_formset,
        'job_formset': job_formset,
        'soft_skill_formset': soft_skill_formset,
    })


def cv_detail(request, id):
    cv = get_object_or_404(CV, id=id, user=request.user)  # Ensure the user is authenticated
    return render(request, 'cv_detail.html', {'cv': cv})
