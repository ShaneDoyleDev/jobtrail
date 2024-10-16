from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


# Contact Details
class ContactDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contact_details")
    name = models.CharField(max_length=255, verbose_name="Full Name")
    linkedin_profile = models.URLField(verbose_name="LinkedIn Profile", blank=True)
    email = models.EmailField(verbose_name="Email Address")
    phone_number = models.CharField(
        max_length=15, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')], 
        verbose_name="Phone Number"
    )
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_contact_details_per_user')
        ]


# Personal Profile
class PersonalProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personal_profiles")
    description = models.TextField(verbose_name="Profile Description")

    def __str__(self):
        return self.description[:50]


# Education
class EducationItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="education_items")
    start_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)], 
        verbose_name="Start Year"
    )
    end_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)], 
        verbose_name="End Year", blank=True, null=True
    )
    school = models.CharField(max_length=255, verbose_name="School Name")
    area_of_study = models.CharField(max_length=255, verbose_name="Area of Study")
    result = models.CharField(max_length=100, verbose_name="Result")

    def __str__(self):
        return f"{self.school} ({self.start_year} - {self.end_year})"


# Hackathons
class HackathonItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hackathon_items")
    year_month = models.DateField(verbose_name="Year/Month")
    github_link = models.URLField(verbose_name="GitHub Link")
    hosts = models.CharField(max_length=255, verbose_name="Host Organization")
    competition_name = models.CharField(max_length=255, verbose_name="Competition Name")
    role = models.CharField(max_length=255, verbose_name="Role")

    def __str__(self):
        return f"{self.competition_name} ({self.year_month})"


# Technical Skills
class ProjectSkill(models.Model):
    skill = models.CharField(max_length=255, verbose_name="Skill")

    def __str__(self):
        return self.skill


# Projects
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    project_name = models.CharField(max_length=255, verbose_name="Project Name")
    live_link = models.URLField(verbose_name="Live Link", blank=True)
    github_link = models.URLField(verbose_name="GitHub Link", blank=True)
    skills = models.ManyToManyField(ProjectSkill, blank=True)
    description = models.TextField(verbose_name="Project Description")

    def __str__(self):
        return self.project_name

# Professional Experience
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    job_title = models.CharField(max_length=255, verbose_name="Job Title")
    company = models.CharField(max_length=255, verbose_name="Company Name")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date", null=True, blank=True)
    bullet_point_1 = models.CharField(max_length=70)
    bullet_point_2 = models.CharField(max_length=70)
    bullet_point_3 = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.job_title} at {self.company}"


# Soft Skills
class SoftSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="soft_skills")
    group_name = models.CharField(max_length=255, verbose_name="Skill Group")
    short_description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.group_name


# Full CV
class CV(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cv")
    contact_details = models.OneToOneField(ContactDetails, on_delete=models.CASCADE)
    personal_profile = models.OneToOneField(PersonalProfile, on_delete=models.CASCADE)
    education_items = models.ManyToManyField(EducationItem, blank=True)
    hackathon_items = models.ManyToManyField(HackathonItem, blank=True)
    technical_skills = models.ManyToManyField(ProjectSkill, blank=True)
    projects = models.ManyToManyField(Project, blank=True)
    jobs = models.ManyToManyField(Job, blank=True)
    soft_skills = models.ManyToManyField(SoftSkill, blank=True)

    def __str__(self):
        return f"CV of {self.contact_details.name}"
