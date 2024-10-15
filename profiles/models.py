import datetime
from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField(default=datetime.date.today)
    reason_for_searching = models.TextField()
    follow_up_no_of_days = models.IntegerField(default=7)

    def __str__(self):
        return self.user.username