from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from .models import CV, ContactDetails, PersonalProfile, EducationItem, HackathonItem, ProjectSkill, Project, Job, SoftSkill
from .forms import (
    ContactDetailsForm, EducationItemForm, HackathonItemForm, JobForm, PersonalProfileForm, EducationFormSet, HackathonFormSet, ProjectForm,
    ProjectFormSet, JobFormSet, ProjectSkillForm, SoftSkillForm, SoftSkillFormSet
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



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

def edit_cv(request, cv_id):
    # Fetch the CV instance by ID or raise a 404 if it doesn't exist
    cv = get_object_or_404(CV, id=cv_id, user=request.user)
    contact_details = cv.contact_details

    if request.method == 'POST':
        contact_form = ContactDetailsForm(request.POST, instance=contact_details)
        profile_form = PersonalProfileForm(request.POST, instance=cv.personal_profile)

        # Formsets
        education_formset = EducationFormSet(request.POST, prefix='education')
        hackathon_formset = HackathonFormSet(request.POST, prefix='hackathon')
        project_formset = ProjectFormSet(request.POST, prefix='projects')
        job_formset = JobFormSet(request.POST, prefix='jobs')
        soft_skill_formset = SoftSkillFormSet(request.POST, prefix='softskills')

        # Validate forms and formsets
        if contact_form.is_valid() and profile_form.is_valid() and all(
            formset.is_valid() for formset in [
                education_formset, hackathon_formset, project_formset, job_formset, soft_skill_formset
            ]
        ):
            # Save contact details and personal profile
            contact_details = contact_form.save(commit=False)
            contact_details.user = request.user
            contact_details.save()

            personal_profile = profile_form.save(commit=False)
            personal_profile.user = request.user
            personal_profile.save()

            # Update the existing CV with new data
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

            return redirect('cv_detail', id=cv.id)  # Redirect to CV detail view after saving
    else:
        # Pre-populate forms and formsets with existing data
        contact_form = ContactDetailsForm(instance=contact_details)
        profile_form = PersonalProfileForm(instance=cv.personal_profile)
        education_formset = EducationFormSet(queryset=EducationItem.objects.filter(user=request.user), prefix='education')
        hackathon_formset = HackathonFormSet(queryset=HackathonItem.objects.filter(user=request.user), prefix='hackathon')
        project_formset = ProjectFormSet(queryset=Project.objects.filter(user=request.user), prefix='projects')
        job_formset = JobFormSet(queryset=Job.objects.filter(user=request.user), prefix='jobs')
        soft_skill_formset = SoftSkillFormSet(queryset=SoftSkill.objects.filter(user=request.user), prefix='softskills')

    return render(request, 'edit_cv.html', {
        'contact_form': contact_form,
        'profile_form': profile_form,
        'education_formset': education_formset,
        'hackathon_formset': hackathon_formset,
        'project_formset': project_formset,
        'job_formset': job_formset,
        'soft_skill_formset': soft_skill_formset,
        'cv': cv,  # Pass CV instance for context (optional)
    })


def cv_detail(request, id):
    cv = get_object_or_404(CV, id=id, user=request.user)  # Ensure the user is authenticated
    return render(request, 'cv_detail.html', {'cv': cv})

class DynamicTitleMixin:
    """Mixin to add a model_name context variable dynamically."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the model name as a context variable
        context['model_name'] = self.model._meta.verbose_name.title()  # Model name in title format
        return context

def create_contact(request):
    contact_details, _ = ContactDetails.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ContactDetailsForm(request.POST, instance=contact_details)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or wherever you want to redirect
    else:
        form = ContactDetailsForm(instance=contact_details)
    return render(request, 'inidvidual/contact_form.html', {'form': form})


# # Contact Details Views
# class ContactDetailsCreateView(DynamicTitleMixin, CreateView):
#     model = ContactDetails
#     form_class = ContactDetailsForm
#     template_name = 'inidvidual/abstract_form.html'
#     success_url = reverse_lazy('dashboard')

class ContactDetailsUpdateView(DynamicTitleMixin, UpdateView):
    model = ContactDetails
    form_class = ContactDetailsForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')


# Personal Profile Views
class PersonalProfileCreateView(DynamicTitleMixin, CreateView):
    model = PersonalProfile
    form_class = PersonalProfileForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Add the user to the form instance
        form.instance.user = self.request.user  # Assuming there's a 'user' field in the PersonalProfile model
        return super().form_valid(form)

class PersonalProfileUpdateView(DynamicTitleMixin, UpdateView):
    model = PersonalProfile
    form_class = PersonalProfileForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')


# Education Item Views
class EducationItemCreateView(DynamicTitleMixin, CreateView):
    model = EducationItem
    form_class = EducationItemForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Add the user to the form instance
        form.instance.user = self.request.user  # Assuming there's a 'user' field in the PersonalProfile model
        return super().form_valid(form)

class EducationItemUpdateView(DynamicTitleMixin, UpdateView):
    model = EducationItem
    form_class = EducationItemForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')


# Hackathon Item Views
class HackathonItemCreateView(DynamicTitleMixin, CreateView):
    model = HackathonItem
    form_class = HackathonItemForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Add the user to the form instance
        form.instance.user = self.request.user  # Assuming there's a 'user' field in the PersonalProfile model
        return super().form_valid(form)

class HackathonItemUpdateView(DynamicTitleMixin, UpdateView):
    model = HackathonItem
    form_class = HackathonItemForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')


# Project Skill Views
class ProjectSkillCreateView(DynamicTitleMixin, CreateView):
    model = ProjectSkill
    form_class = ProjectSkillForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Add the user to the form instance
        form.instance.user = self.request.user  # Assuming there's a 'user' field in the PersonalProfile model
        return super().form_valid(form)

class ProjectSkillUpdateView(DynamicTitleMixin, UpdateView):
    model = ProjectSkill
    form_class = ProjectSkillForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')


# Project Views
class ProjectCreateView(DynamicTitleMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Add the user to the form instance
        form.instance.user = self.request.user  # Assuming there's a 'user' field in the PersonalProfile model
        return super().form_valid(form)

class ProjectUpdateView(DynamicTitleMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')


# Job Views
class JobCreateView(DynamicTitleMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Add the user to the form instance
        form.instance.user = self.request.user  # Assuming there's a 'user' field in the PersonalProfile model
        return super().form_valid(form)

class JobUpdateView(DynamicTitleMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')


# Soft Skill Views
class SoftSkillCreateView(DynamicTitleMixin, CreateView):
    model = SoftSkill
    form_class = SoftSkillForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Add the user to the form instance
        form.instance.user = self.request.user  # Assuming there's a 'user' field in the PersonalProfile model
        return super().form_valid(form)

class SoftSkillUpdateView(DynamicTitleMixin, UpdateView):
    model = SoftSkill
    form_class = SoftSkillForm
    template_name = 'inidvidual/abstract_form.html'
    success_url = reverse_lazy('dashboard')


class ContactDetailsListView(LoginRequiredMixin, ListView):
    model = ContactDetails
    template_name = 'list/contactdetails_list.html'
    context_object_name = 'contact_details'

    def get_queryset(self):
        return self.request.user.contact_details.all()


class PersonalProfileListView(LoginRequiredMixin, ListView):
    model = PersonalProfile
    template_name = 'list/personalprofile_list.html'
    context_object_name = 'personal_profiles'

    def get_queryset(self):
        return self.request.user.personal_profiles.all()


class EducationItemListView(LoginRequiredMixin, ListView):
    model = EducationItem
    template_name = 'list/educationitem_list.html'
    context_object_name = 'education_items'

    def get_queryset(self):
        return self.request.user.education_items.all()


class HackathonItemListView(LoginRequiredMixin, ListView):
    model = HackathonItem
    template_name = 'list/hackathonitem_list.html'
    context_object_name = 'hackathon_items'

    def get_queryset(self):
        return self.request.user.hackathon_items.all()


class ProjectSkillListView(LoginRequiredMixin, ListView):
    model = ProjectSkill
    template_name = 'list/projectskill_list.html'
    context_object_name = 'project_skills'


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'list/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return self.request.user.projects.all()


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'list/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.request.user.jobs.all()


class SoftSkillListView(LoginRequiredMixin, ListView):
    model = SoftSkill
    template_name = 'list/softskill_list.html'
    context_object_name = 'soft_skills'

    def get_queryset(self):
        return self.request.user.soft_skills.all()


class CVListView(LoginRequiredMixin, ListView):
    model = CV
    template_name = 'list/cv_list.html'
    context_object_name = 'cvs'

    def get_queryset(self):
        cvs = CV.objects.filter(user=self.request.user)
        return cvs

@login_required
def select_cv_elements(request):
    user = request.user
    cv, created = CV.objects.get_or_create(user=user)  # Get or create the user's CV

    # Fetch user items
    education_items = EducationItem.objects.filter(user=user)
    hackathon_items = HackathonItem.objects.filter(user=user)
    projects = Project.objects.filter(user=user)
    jobs = Job.objects.filter(user=user)
    soft_skills = SoftSkill.objects.filter(user=user)
    personal_profiles = PersonalProfile.objects.filter(user=user)

    # Prepare lists of selected IDs
    selected_education_ids = list(cv.education_items.values_list('id', flat=True))
    selected_hackathon_ids = list(cv.hackathon_items.values_list('id', flat=True))
    selected_project_ids = list(cv.projects.values_list('id', flat=True))
    selected_job_ids = list(cv.jobs.values_list('id', flat=True))
    selected_soft_skill_ids = list(cv.soft_skills.values_list('id', flat=True))
    selected_personal_profile_id = cv.personal_profile_id

    if request.method == 'POST':
        # Get selected items from the form
        selected_personal_profile = request.POST.get('personal_profile')
        selected_education = request.POST.getlist('education_items')
        selected_hackathons = request.POST.getlist('hackathon_items')
        selected_projects = request.POST.getlist('projects')
        selected_jobs = request.POST.getlist('jobs')
        selected_soft_skills = request.POST.getlist('soft_skills')

        # Update the CV instance
        if selected_personal_profile:
            cv.personal_profile_id = selected_personal_profile

        cv.education_items.clear()
        for item_id in selected_education:
            if item_id:
                cv.education_items.add(item_id)

        cv.hackathon_items.clear()
        for item_id in selected_hackathons:
            if item_id:
                cv.hackathon_items.add(item_id)

        cv.projects.clear()
        for item_id in selected_projects:
            if item_id:
                cv.projects.add(item_id)

        cv.jobs.clear()
        for item_id in selected_jobs:
            if item_id:
                cv.jobs.add(item_id)

        cv.soft_skills.clear()
        for item_id in selected_soft_skills:
            if item_id:
                cv.soft_skills.add(item_id)

        cv.save()
        return redirect('cv_detail', cv.id)  # Redirect to CV detail view

    context = {
        'education_items': education_items,
        'hackathon_items': hackathon_items,
        'projects': projects,
        'jobs': jobs,
        'soft_skills': soft_skills,
        'personal_profiles': personal_profiles,
        'cv': cv,
        'selected_education_ids': selected_education_ids,
        'selected_hackathon_ids': selected_hackathon_ids,
        'selected_project_ids': selected_project_ids,
        'selected_job_ids': selected_job_ids,
        'selected_soft_skill_ids': selected_soft_skill_ids,
        'selected_personal_profile_id': selected_personal_profile_id,
    }
    return render(request, 'select_cv_elements.html', context)
