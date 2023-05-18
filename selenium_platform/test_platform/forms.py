from django import forms
from django.forms.widgets import ClearableFileInput, FileInput
from .models import TestCase


class TestUploadForm(forms.ModelForm):
    #file = forms.FileField(widget=FileInput(attrs={'style': 'background-color: yellow;'}), )

    class Meta:
        model = TestCase
        fields = ('name', 'file')
        #widgets = {
        #    'file': forms.FileInput(attrs={'class': 'custom-file-input.custom-file-input'}),
        #}


class EditCodeForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea(attrs={'rows':20, 'cols':130}))

class EditTestNameForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }