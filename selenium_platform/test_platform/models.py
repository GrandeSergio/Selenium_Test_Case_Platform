from django.db import models
from django.utils import timezone

class TestCase(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='test_cases')
    last_run_status = models.CharField(max_length=10, blank=True, null=True)
    console_output = models.TextField(blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    last_run_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
