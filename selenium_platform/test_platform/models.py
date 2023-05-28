from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class TestCase(models.Model):
    #user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='test_cases')
    last_run_status = models.CharField(max_length=10, blank=True, null=True)
    console_output = models.TextField(blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    last_run_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class TestRun(models.Model):
    test = models.ForeignKey('TestCase', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20)
    output = models.TextField()

    def __str__(self):
        return f"{self.test.name} - {self.status} - {self.date}"
'''
class CustomUser(AbstractUser):
    # Add any additional fields you want for your user model
    # For example, you can add a profile picture field:
    # profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.username
'''