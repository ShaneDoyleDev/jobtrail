from django import forms
from django.forms import inlineformset_factory
from .models import CV, ContactDetails, PersonalProfile, Education, EducationItem, Hackathons, HackathonItem, TechnicalSkills, TechnicalSkill, Projects, Project, Job, JobBulletPoint, ProfessionalExperience, SoftSkills, SoftSkill

# Individual Forms
class ContactDetailsForm(forms.ModelForm):
    class Meta:
        model = ContactDetails
        fields = '__all__'

class PersonalProfileForm(forms.ModelForm):
    class Meta:
        model = PersonalProfile
        fields = '__all__'

# Formsets for related models
EducationItemFormset = inlineformset_factory(Education, EducationItem, fields='__all__', extra=1, can_delete=True)
# HackathonItem Formset with custom DateInput widget for the year_month field
HackathonItemFormset = inlineformset_factory(
    Hackathons, HackathonItem, 
    fields='__all__', 
    extra=1, 
    can_delete=True,
    widgets={
        'year_month': forms.DateInput(attrs={'type': 'date'}),
    }
)
TechnicalSkillFormset = inlineformset_factory(TechnicalSkills, TechnicalSkill, fields='__all__', extra=1, can_delete=True)
ProjectFormset = inlineformset_factory(Projects, Project, fields='__all__', extra=1, can_delete=True)
# Job Formset with custom DateInput widget for the start and end date field
JobFormset = inlineformset_factory(
    Hackathons, HackathonItem, 
    fields='__all__', 
    extra=1, 
    can_delete=True,
    widgets={
        'start_date': forms.DateInput(attrs={'type': 'date'}),
        'end_date': forms.DateInput(attrs={'type': 'date'}),
    }
)
JobBulletPointFormset = inlineformset_factory(Job, JobBulletPoint, fields='__all__', extra=3, can_delete=True)
SoftSkillFormset = inlineformset_factory(SoftSkills, SoftSkill, fields='__all__', extra=1, can_delete=True)
