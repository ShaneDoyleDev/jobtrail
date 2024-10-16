# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import CV, ContactDetails, PersonalProfile, EducationItem, HackathonItem, ProjectSkill, Project, Job, SoftSkill

class ContactDetailsForm(forms.ModelForm):
    class Meta:
        model = ContactDetails
        fields = ['name', 'linkedin_profile', 'email', 'phone_number', 'location']


class PersonalProfileForm(forms.ModelForm):
    class Meta:
        model = PersonalProfile
        fields = ['description']


class EducationItemForm(forms.ModelForm):
    # Create a list of years from 1924 to 2024
    YEAR_CHOICES = [(year, year) for year in range(2024, 1923, -1)]

    start_year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select, label='Start Year')
    end_year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select, label='End Year')

    class Meta:
        model = EducationItem
        fields = ['start_year', 'end_year', 'school', 'area_of_study', 'result']


class HackathonItemForm(forms.ModelForm):
    year_month = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month'}),
        label='Year and Month'
    )

    class Meta:
        model = HackathonItem
        fields = ['year_month', 'github_link', 'hosts', 'competition_name', 'role']


class ProjectSkillForm(forms.ModelForm):
    class Meta:
        model = ProjectSkill
        fields = ['skill']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'live_link', 'github_link', 'skills', 'description']


class JobForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month'}),
        label='Start Date'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month'}),
        label='End Date'
    )

    class Meta:
        model = Job
        fields = ['job_title', 'company', 'start_date', 'end_date', 'bullet_point_1', 'bullet_point_2', 'bullet_point_3']


class SoftSkillForm(forms.ModelForm):
    class Meta:
        model = SoftSkill
        fields = ['group_name', 'short_description']


# Formsets for ManyToMany fields
EducationFormSet = modelformset_factory(EducationItem, form=EducationItemForm, extra=1, can_delete=True)
HackathonFormSet = modelformset_factory(HackathonItem, form=HackathonItemForm, extra=1, can_delete=True)
ProjectSkillFormSet = modelformset_factory(ProjectSkill, form=ProjectSkillForm, extra=1, can_delete=True)
ProjectFormSet = modelformset_factory(Project, form=ProjectForm, extra=1, can_delete=True)
JobFormSet = modelformset_factory(Job, form=JobForm, extra=1, can_delete=True)
SoftSkillFormSet = modelformset_factory(SoftSkill, form=SoftSkillForm, extra=1, can_delete=True)
