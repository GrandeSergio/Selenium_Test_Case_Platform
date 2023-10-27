from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class TestCase(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='test_cases')
    last_run_status = models.CharField(max_length=10, blank=True, null=True)
    console_output = models.TextField(blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    last_run_date = models.DateTimeField(null=True, blank=True)

    def get_formatted_upload_date(self):
        return self.upload_date.strftime("%d-%m-%Y %H:%M:%S")

    def __str__(self):
        return self.name


class SchedulerRun(models.Model):
    scheduler = models.ForeignKey('Scheduler', on_delete=models.CASCADE, related_name='scheduler_runs')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    test_runs = models.ManyToManyField('TestRun')

    def __str__(self):
        return f"Scheduler Run {self.id} - {self.date}"


class TestRun(models.Model):
    test = models.ForeignKey('TestCase', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20)
    output = models.TextField()
    scheduler_run = models.ForeignKey(SchedulerRun, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.test.name} - {self.status} - {self.date}"


class Scheduler(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    test_cases = models.ManyToManyField('TestCase')
    created_at = models.DateTimeField(default=timezone.now)
    last_run_date = models.DateTimeField(null=True, blank=True)
    # Add other fields as needed

    def __str__(self):
        return self.name


