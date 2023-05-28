from django import forms
from django.forms.widgets import ClearableFileInput, FileInput
from .models import TestCase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']