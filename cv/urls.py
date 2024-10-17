from django.urls import path
from . import views
from django.urls import path
from .views import (
    ContactDetailsUpdateView,
    PersonalProfileCreateView,
    PersonalProfileUpdateView,
    EducationItemCreateView,
    EducationItemUpdateView,
    HackathonItemCreateView,
    HackathonItemUpdateView,
    ProjectSkillCreateView,
    ProjectSkillUpdateView,
    ProjectCreateView,
    ProjectUpdateView,
    JobCreateView,
    JobUpdateView,
    SoftSkillCreateView,
    SoftSkillUpdateView,
    ContactDetailsListView,
    PersonalProfileListView,
    EducationItemListView,
    HackathonItemListView,
    ProjectSkillListView,
    ProjectListView,
    JobListView,
    SoftSkillListView,
    CVListView,
)

urlpatterns = [
    path("create/", views.create_cv, name="create_cv"),
    path("generate_pdf/", views.generate_pdf, name="generate_pdf"),
    path("cv_detail/<int:id>/", views.cv_detail, name="cv_detail"),
    # Contact Details
    # path('contact-details/new/', ContactDetailsCreateView.as_view(), name='contact_details_create'),
    path("contact-details/", views.create_contact, name="contact_details_edit"),
    # Personal Profile
    path(
        "personal-profile/new/",
        PersonalProfileCreateView.as_view(),
        name="personal_profile_create",
    ),
    path(
        "personal-profile/<int:pk>/edit/",
        PersonalProfileUpdateView.as_view(),
        name="personal_profile_edit",
    ),
    # Education Item
    path(
        "education-item/new/",
        EducationItemCreateView.as_view(),
        name="education_item_create",
    ),
    path(
        "education-item/<int:pk>/edit/",
        EducationItemUpdateView.as_view(),
        name="education_item_edit",
    ),
    # Hackathon Item
    path(
        "hackathon-item/new/",
        HackathonItemCreateView.as_view(),
        name="hackathon_item_create",
    ),
    path(
        "hackathon-item/<int:pk>/edit/",
        HackathonItemUpdateView.as_view(),
        name="hackathon_item_edit",
    ),
    # Project Skill
    path(
        "project-skill/new/",
        ProjectSkillCreateView.as_view(),
        name="project_skill_create",
    ),
    path(
        "project-skill/<int:pk>/edit/",
        ProjectSkillUpdateView.as_view(),
        name="project_skill_edit",
    ),
    # Project
    path("project/new/", ProjectCreateView.as_view(), name="project_create"),
    path("project/<int:pk>/edit/", ProjectUpdateView.as_view(), name="project_edit"),
    # Job
    path("job/new/", JobCreateView.as_view(), name="job_create"),
    path("edit/<int:cv_id>/", views.edit_cv, name="cv_edit"),
    path("job/new/", JobUpdateView.as_view(), name="job_edit"),
    # Soft Skill
    path("soft-skill/new/", SoftSkillCreateView.as_view(), name="soft_skill_create"),
    path(
        "soft-skill/<int:pk>/edit/",
        SoftSkillUpdateView.as_view(),
        name="soft_skill_edit",
    ),
        # Edits

    path(
        "contact-details/",
        ContactDetailsListView.as_view(),
        name="contact-details-list",
    ),
    path(
        "personal-profiles/",
        PersonalProfileListView.as_view(),
        name="personal-profile-list",
    ),
    path(
        "education-items/", EducationItemListView.as_view(), name="education-item-list"
    ),
    path(
        "hackathon-items/", HackathonItemListView.as_view(), name="hackathon-item-list"
    ),
    path("project-skills/", ProjectSkillListView.as_view(), name="project-skill-list"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("jobs/", JobListView.as_view(), name="job-list"),
    path("soft-skills/", SoftSkillListView.as_view(), name="soft-skill-list"),
    path("cvs/", CVListView.as_view(), name="cv_list"),
    path('select-cv-elements/', views.select_cv_elements, name='select_cv_elements'),
]
