from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    reason_for_searching = models.TextField()
    follow_up_no_of_days = models.IntegerField(default=7)

    def __str__(self):
        return self.username