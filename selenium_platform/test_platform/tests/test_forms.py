from django.test import TestCase
from django.forms import ValidationError
from django.contrib.auth.models import User
from ..forms import TestUploadForm, EditCodeForm, EditTestNameForm, RegistrationForm, SchedulerForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage


class TestUploadFormTestCase(TestCase):
    def tearDown(self):
        # Delete the files created during the test
        default_storage.delete('unit_test_forms.py')

    def test_form_valid(self):
        file_data = b'Test file content'
        form = TestUploadForm(data={'name': 'Unit Test Case Forms 1'}, files={'file': SimpleUploadedFile('unit_test_forms.py', file_data)})
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors.as_data()}")

    def test_form_invalid(self):
        form = TestUploadForm(data={})
        self.assertFalse(form.is_valid(), f"Form errors: {form.errors.as_data()}")



class EditCodeFormTestCase(TestCase):
    def test_form_valid(self):
        form = EditCodeForm(data={'code': 'print("Hello, World!")'})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = EditCodeForm(data={})
        self.assertFalse(form.is_valid())


class EditTestNameFormTestCase(TestCase):
    def test_form_valid(self):
        form = EditTestNameForm(data={'name': 'New Test Name'})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = EditTestNameForm(data={})
        self.assertFalse(form.is_valid())


class RegistrationFormTestCase(TestCase):
    def test_form_valid(self):
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = RegistrationForm(data={})
        self.assertFalse(form.is_valid())

    def test_form_password_mismatch(self):
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'mismatchedpass'
        })
        self.assertFalse(form.is_valid())


class SchedulerFormTestCase(TestCase):
    def test_form_valid(self):
        form = SchedulerForm(data={'name': 'Test Scheduler'})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = SchedulerForm(data={})
        self.assertFalse(form.is_valid())
