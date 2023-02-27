from django import forms
from .models import TestCase

class TestUploadForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ('name', 'file')

