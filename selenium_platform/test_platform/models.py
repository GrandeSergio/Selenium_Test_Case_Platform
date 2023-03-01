from django.db import models

class TestCase(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='test_cases')
    last_run_status = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name
