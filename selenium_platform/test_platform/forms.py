from django import forms
from .models import TestCase


class TestUploadForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ('name', 'file')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'custom-file-input.custom-file-input'}),
        }
