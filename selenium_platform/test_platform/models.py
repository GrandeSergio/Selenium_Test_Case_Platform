from django.db import models

class TestCase(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='test_cases')

    def __str__(self):
        return self.name
