from django.db import models


# Contact Details
class ContactDetails(models.Model):
    name = models.CharField(max_length=255)
    linkedin_profile = models.URLField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Personal Profile
class PersonalProfile(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description[:50]


class Education(models.Model):

    pass

# Education
class EducationItem(models.Model):
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    school = models.CharField(max_length=255)
    area_of_study = models.CharField(max_length=255)
    result = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.school} ({self.start_year} - {self.end_year})"
    

class Hackathons(models.Model):

    pass


# Hackathons
class HackathonItem(models.Model):
    hackathons = models.ForeignKey(Hackathons, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    year_month = models.DateField()
    github_link = models.URLField()
    hosts = models.CharField(max_length=255)
    competition_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.competition_name} ({self.year_month})"


class TechnicalSkills(models.Model):
    group_name = models.CharField(max_length=255)

    def __str__(self):
        return self.group_name
    
# Technical Skills
class TechnicalSkill(models.Model):
    technical_skills = models.ForeignKey(TechnicalSkills, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    skill = models.CharField(max_length=255)

    def __str__(self):
        return self.skill


class Projects(models.Model):

    pass


# Projects
class Project(models.Model):
    projects = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    project_name = models.CharField(max_length=255)
    live_link = models.URLField()
    github_link = models.URLField()
    skills = models.ManyToManyField(TechnicalSkill, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.project_name



class ProfessionalExperience(models.Model):

    pass


class Job(models.Model):
    professional_experience = models.ForeignKey(ProfessionalExperience, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.job_title
    
# Professional Experience
class JobBulletPoint(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    jbp = models.TextField()

    def __str__(self):
        return self.jbp[:50]


class SoftSkills(models.Model):

    pass

# Soft Skills
class SoftSkill(models.Model):
    soft_skills = models.ForeignKey(SoftSkills, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    group_name = models.CharField(max_length=255)
    short_description = models.TextField()

    def __str__(self):
        return self.group_name

# Full CV
class CV(models.Model):
    contact_details = models.OneToOneField(ContactDetails, on_delete=models.CASCADE)
    personal_profile = models.OneToOneField(PersonalProfile, on_delete=models.CASCADE)
    education = models.OneToOneField(Education, on_delete=models.CASCADE)
    hackathons = models.OneToOneField(Hackathons, on_delete=models.CASCADE)
    technical_skills = models.OneToOneField(TechnicalSkills, on_delete=models.CASCADE)
    projects = models.OneToOneField(Projects, on_delete=models.CASCADE)
    professional_experience = models.OneToOneField(ProfessionalExperience, on_delete=models.CASCADE)
    soft_skills = models.OneToOneField(SoftSkills, on_delete=models.CASCADE)

    def __str__(self):
        return f"CV of {self.contact_details.name}"
