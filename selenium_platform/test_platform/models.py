from django.db import models

class TestCase(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='testcases/')

    def __str__(self):
        return self.name
