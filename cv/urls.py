from django.urls import path
from . import views
from django.urls import path
from .views import (
    PersonalProfileCreateView, PersonalProfileUpdateView,
    EducationItemCreateView, EducationItemUpdateView,
    HackathonItemCreateView, HackathonItemUpdateView,
    ProjectSkillCreateView, ProjectSkillUpdateView,
    ProjectCreateView, ProjectUpdateView,
    JobCreateView, JobUpdateView,
    SoftSkillCreateView, SoftSkillUpdateView
)

urlpatterns = [
    path('create/', views.create_cv, name='create_cv'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('cv_detail/<int:id>/', views.cv_detail, name='cv_detail'),

    # Contact Details
    # path('contact-details/new/', ContactDetailsCreateView.as_view(), name='contact_details_create'),
    path('contact-details/', views.create_contact, name='contact_details_edit'),

    # Personal Profile
    path('personal-profile/new/', PersonalProfileCreateView.as_view(), name='personal_profile_create'),
    path('personal-profile/<int:pk>/edit/', PersonalProfileUpdateView.as_view(), name='personal_profile_edit'),

    # Education Item
    path('education-item/new/', EducationItemCreateView.as_view(), name='education_item_create'),
    path('education-item/<int:pk>/edit/', EducationItemUpdateView.as_view(), name='education_item_edit'),

    # Hackathon Item
    path('hackathon-item/new/', HackathonItemCreateView.as_view(), name='hackathon_item_create'),
    path('hackathon-item/<int:pk>/edit/', HackathonItemUpdateView.as_view(), name='hackathon_item_edit'),

    # Project Skill
    path('project-skill/new/', ProjectSkillCreateView.as_view(), name='project_skill_create'),
    path('project-skill/<int:pk>/edit/', ProjectSkillUpdateView.as_view(), name='project_skill_edit'),

    # Project
    path('project/new/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),

    # Job
    path('job/new/', JobCreateView.as_view(), name='job_create'),
    path('job/<int:pk>/edit/', JobUpdateView.as_view(), name='job_edit'),

    # Soft Skill
    path('soft-skill/new/', SoftSkillCreateView.as_view(), name='soft_skill_create'),
    path('soft-skill/<int:pk>/edit/', SoftSkillUpdateView.as_view(), name='soft_skill_edit'),
]
