from django import forms
from .models import TestCase, Scheduler
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TestUploadForm(forms.ModelForm):

    class Meta:
        model = TestCase
        fields = ('name', 'file')


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

class SchedulerForm(forms.ModelForm):
    class Meta:
        model = Scheduler
        fields = ['name']