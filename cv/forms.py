# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import CV, ContactDetails, PersonalProfile, EducationItem, HackathonItem, TechnicalSkill, Project, Job, SoftSkill


class ContactDetailsForm(forms.ModelForm):
    class Meta:
        model = ContactDetails
        fields = ['name', 'linkedin_profile', 'email', 'phone_number', 'location']


class PersonalProfileForm(forms.ModelForm):
    class Meta:
        model = PersonalProfile
        fields = ['description']


class EducationItemForm(forms.ModelForm):
    class Meta:
        model = EducationItem
        fields = ['start_year', 'end_year', 'school', 'area_of_study', 'result']


class HackathonItemForm(forms.ModelForm):
    class Meta:
        model = HackathonItem
        fields = ['year_month', 'github_link', 'hosts', 'competition_name', 'role']


class TechnicalSkillForm(forms.ModelForm):
    class Meta:
        model = TechnicalSkill
        fields = ['skill']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'live_link', 'github_link', 'skills', 'description']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_title', 'company', 'start_date', 'end_date']


class SoftSkillForm(forms.ModelForm):
    class Meta:
        model = SoftSkill
        fields = ['group_name', 'short_description']


# Formsets for ManyToMany fields
EducationFormSet = modelformset_factory(EducationItem, form=EducationItemForm, extra=1, can_delete=True)
HackathonFormSet = modelformset_factory(HackathonItem, form=HackathonItemForm, extra=1, can_delete=True)
TechnicalSkillFormSet = modelformset_factory(TechnicalSkill, form=TechnicalSkillForm, extra=1, can_delete=True)
ProjectFormSet = modelformset_factory(Project, form=ProjectForm, extra=1, can_delete=True)
JobFormSet = modelformset_factory(Job, form=JobForm, extra=1, can_delete=True)
SoftSkillFormSet = modelformset_factory(SoftSkill, form=SoftSkillForm, extra=1, can_delete=True)

# HackathonItem Formset with custom DateInput widget for the year_month field
# HackathonItemFormset = inlineformset_factory(
#     Hackathons, HackathonItem, 
#     fields='__all__', 
#     extra=1, 
#     can_delete=True,
#     widgets={
#         'year_month': forms.DateInput(attrs={'type': 'date'}),
#     }
# )
