from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from django.shortcuts import render, redirect
from .forms import ContactDetailsForm, PersonalProfileForm, EducationItemFormset, HackathonItemFormset, TechnicalSkillFormset, ProjectFormset, JobFormset, JobBulletPointFormset, SoftSkillFormset
from .models import CV, Education, Hackathons, TechnicalSkills, Projects, ProfessionalExperience, SoftSkills

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
    if request.method == 'POST':
        # Main forms
        contact_details_form = ContactDetailsForm(request.POST)
        personal_profile_form = PersonalProfileForm(request.POST)

        # Formsets
        education_formset = EducationItemFormset(request.POST, prefix='education')
        hackathon_formset = HackathonItemFormset(request.POST, prefix='hackathons')
        technical_skill_formset = TechnicalSkillFormset(request.POST, prefix='techskills')
        project_formset = ProjectFormset(request.POST, prefix='projects')
        job_formset = JobFormset(request.POST, prefix='jobs')
        soft_skill_formset = SoftSkillFormset(request.POST, prefix='softskills')
        
        print(contact_details_form.is_valid())
        print(personal_profile_form.is_valid())
        print(education_formset.is_valid())
        print(hackathon_formset.is_valid())
        print(technical_skill_formset.is_valid())
        print(project_formset.is_valid())
        print(job_formset.is_valid())
        print(soft_skill_formset.is_valid())

        if (contact_details_form.is_valid() and personal_profile_form.is_valid() and
            education_formset.is_valid() and hackathon_formset.is_valid() and
            technical_skill_formset.is_valid() and project_formset.is_valid() and
            job_formset.is_valid() and soft_skill_formset.is_valid()):
            print("submitted")
            # Save main forms
            contact_details = contact_details_form.save()
            personal_profile = personal_profile_form.save()

            # Create CV
            cv = CV.objects.create(
                contact_details=contact_details,
                personal_profile=personal_profile,
                education=Education.objects.create(),
                hackathons=Hackathons.objects.create(),
                technical_skills=TechnicalSkills.objects.create(),
                projects=Projects.objects.create(),
                professional_experience=ProfessionalExperience.objects.create(),
                soft_skills=SoftSkills.objects.create(),
            )

            # Save formsets to related models
            education_formset.instance = cv.education
            education_formset.save()

            hackathon_formset.instance = cv.hackathons
            hackathon_formset.save()

            technical_skill_formset.instance = cv.technical_skills
            technical_skill_formset.save()

            project_formset.instance = cv.projects
            project_formset.save()

            job_formset.instance = cv.professional_experience
            job_formset.save()

            soft_skill_formset.instance = cv.soft_skills
            soft_skill_formset.save()
            
            template = get_template('pdf_template.html')
            context = {'cv': cv}
            html_content = template.render(context)

            # Create a PDF using WeasyPrint
            pdf = HTML(string=html_content).write_pdf()

            # Return the PDF as a downloadable response
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            return redirect('dashboard')
    else:
        # Empty forms for GET request
        contact_details_form = ContactDetailsForm()
        personal_profile_form = PersonalProfileForm()
        education_formset = EducationItemFormset(prefix='education')
        hackathon_formset = HackathonItemFormset(prefix='hackathons')
        technical_skill_formset = TechnicalSkillFormset(prefix='techskills')
        project_formset = ProjectFormset(prefix='projects')
        job_formset = JobFormset(prefix='jobs')
        soft_skill_formset = SoftSkillFormset(prefix='softskills')

    return render(request, 'create_cv.html', {
        'contact_details_form': contact_details_form,
        'personal_profile_form': personal_profile_form,
        'education_formset': education_formset,
        'hackathon_formset': hackathon_formset,
        'technical_skill_formset': technical_skill_formset,
        'project_formset': project_formset,
        'job_formset': job_formset,
        'soft_skill_formset': soft_skill_formset,
    })
