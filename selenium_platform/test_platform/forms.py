from django import forms
from .models import TestCase
from django.forms import FileInput
from django.utils.translation import gettext_lazy as _


class TestUploadForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ('name', 'file')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'custom-file-input.custom-file-input'}),
        }
