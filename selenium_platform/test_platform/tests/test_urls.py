from django.test import TestCase, Client
from django.urls import reverse, resolve
from .. import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User


class URLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('testpass')
        self.user.save()
        self.client = Client()
        self.logged_in = self.client.login(username='testuser', password='testpass')
    def test_test_list_url(self):
        url = reverse('test_list')
        self.assertEqual(resolve(url).func, views.test_list)

    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_test_details_url(self):
        url = reverse('test_details', args=[1])
        self.assertEqual(resolve(url).func, views.test_details)

    def test_test_code_url(self):
        url = reverse('test_code', args=[1])
        self.assertEqual(resolve(url).func, views.test_code)

    def test_run_test_cases_url(self):
        url = reverse('run_test_cases', args=[1])
        self.assertEqual(resolve(url).func, views.run_test_cases)

    def test_delete_test_case_url(self):
        url = reverse('delete_test_case', args=[1])
        self.assertEqual(resolve(url).func, views.delete_test_case)

    def test_test_history_url(self):
        url = reverse('test_history', args=[1])
        self.assertEqual(resolve(url).func, views.test_history)

    def test_run_output_url(self):
        url = reverse('run_output', args=[1])
        self.assertEqual(resolve(url).func, views.run_output)

    def test_test_history_list_url(self):
        url = reverse('test_history_list')
        self.assertEqual(resolve(url).func, views.test_history_list)

    def test_replace_file_url(self):
        url = reverse('replace_file', args=[1])
        self.assertEqual(resolve(url).func, views.replace_file)

    def test_upload_url(self):
        url = reverse('upload')
        self.assertEqual(resolve(url).func, views.upload)

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.user_login)

    def test_user_details_url(self):
        url = reverse('user_details')
        self.assertEqual(resolve(url).func, views.user_details)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_delete_account_url(self):
        url = reverse('delete_account')
        self.assertEqual(resolve(url).func, views.delete_account)

    def test_change_password_url(self):
        url = reverse('change_password')
        self.assertEqual(resolve(url).func.view_class, views.CustomPasswordChangeView)

    def test_change_password_done_url(self):
        url = reverse('change_password_done')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_url(self):
        url = reverse('password_reset')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_url(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url(self):
        url = reverse('password_reset_confirm', args=['uidb64', 'token'])
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_complete_url(self):
        url = reverse('password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    def test_scheduler_list_url(self):
        url = reverse('scheduler_list')
        self.assertEqual(resolve(url).func, views.scheduler_list)

    def test_scheduler_details_url(self):
        url = reverse('scheduler_details', args=[1])
        self.assertEqual(resolve(url).func, views.scheduler_details)

    def test_add_test_cases_url(self):
        url = reverse('add_test_cases', args=[1])
        self.assertEqual(resolve(url).func, views.add_test_cases)

    def test_create_scheduler_url(self):
        url = reverse('create_scheduler')
        self.assertEqual(resolve(url).func, views.create_scheduler)

    def test_remove_test_case_url(self):
        url = reverse('remove_test_case', args=[1, 1])
        self.assertEqual(resolve(url).func, views.remove_test_case)

    def test_scheduler_history_url(self):
        url = reverse('scheduler_history', args=[1])
        self.assertEqual(resolve(url).func, views.scheduler_history)

    def test_delete_scheduler_url(self):
        url = reverse('delete_scheduler', args=[1])
        self.assertEqual(resolve(url).func, views.delete_scheduler)

    def test_scheduler_run_history_url(self):
        url = reverse('scheduler_run_history', args=[1])
        self.assertEqual(resolve(url).func, views.scheduler_run_history)