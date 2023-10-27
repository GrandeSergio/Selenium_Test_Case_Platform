from django.test import TestCase, Client
from django.urls import reverse
from ..models import TestCase as TestCaseModel, TestRun, Scheduler, SchedulerRun
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from django.core.files.storage import default_storage


class ViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('testpass')
        self.user.save()
        self.client = Client()
        self.logged_in = self.client.login(username='testuser', password='testpass')
        self.test_case = TestCaseModel.objects.create(name='Test Case Views 1', user=self.user)

        # Create a file for the test case
        file_content = b'Test file content'
        test_file = SimpleUploadedFile('test_file_views.py', file_content)
        self.test_case.file = test_file
        self.test_case.save()

        self.test_run = TestRun.objects.create(test=self.test_case, status='PASSED')

    def tearDown(self):
        # Delete the files created during the test
        default_storage.delete('test_file.py')

    def test_test_list_view(self):
        url = reverse('test_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_list.html')

    def test_test_details_view(self):
        url = reverse('test_details', args=[self.test_case.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_details.html')

    def test_replace_file_view(self):
        url = reverse('replace_file', args=[self.test_case.id])
        file_content = 'This is a test file content.'
        response = self.client.post(url, {'file': file_content}, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('test_details', args=[self.test_case.id]))

    def test_test_code_view(self):
        url = reverse('test_code', args=[self.test_case.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_code.html')
        self.assertEqual(response.context['test'], self.test_case)
        self.assertEqual(response.context['file_content'], 'Test file content')
        self.assertEqual(response.context['active_tab'], 'code')

    def test_test_history_list_view(self):
        url = reverse('test_history_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_history_list.html')

    def test_test_history_view(self):
        url = reverse('test_history', args=[self.test_case.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_history.html')

    def test_run_output_view(self):
        run = TestRun.objects.create(test=self.test_case, status='PASSED')
        url = reverse('run_output', args=[run.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'run_output.html')

    @patch('test_platform.views.execute_test_case')  # Mocking execute_test_case function
    def test_run_test_cases_view(self, mock_execute_test_case):
        url = reverse('run_test_cases', args=[self.test_case.id])
        mode = 'batch'
        output = 'Test output'
        mock_execute_test_case.return_value = output

        # Make a POST request to the view
        response = self.client.post(url, {'mode': mode})

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'output': output})

        # Assert that execute_test_case was called with the correct arguments
        mock_execute_test_case.assert_called_once_with(self.test_case, mode)

    def test_delete_test_case_view(self):
        url = reverse('delete_test_case', args=[self.test_case.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')

    def test_upload_view(self):
        url = reverse('upload')
        name = 'Unit test Test Case Views 1'

        # Delete any existing TestCase objects with the same name
        TestCaseModel.objects.filter(name=name).delete()

        # Create a SimpleUploadedFile object
        file_data = b'Test file content'
        file = SimpleUploadedFile('test_file_views.py', file_data)

        # Make a POST request to the view
        response = self.client.post(url, {'name': name, 'file': file})

        # Assert the response
        self.assertEqual(response.status_code, 200)
        test_cases = TestCaseModel.objects.filter(name=name)
        self.assertEqual(test_cases.count(), 1)
        test_case = test_cases.first()
        test_case_url = reverse('test_details', kwargs={'test_id': test_case.id})
        self.assertJSONEqual(response.content, {'success': True, 'test_case_url': test_case_url})

        # Assert that the test case is created with the correct attributes
        self.assertEqual(test_case.user, self.user)
        self.assertEqual(test_case.name, name)
        self.assertEqual(test_case.file.read(), file_data)

    def test_register_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_user_login_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_details_view(self):
        url = reverse('user_details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_details.html')

    def test_delete_account_view(self):
        url = reverse('delete_account')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_change_password_view(self):
        url = reverse('change_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_scheduler_list_view(self):
        url = reverse('scheduler_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduler_list.html')

    def test_scheduler_details_view(self):
        scheduler = Scheduler.objects.create(name='Test Scheduler', user=self.user)
        url = reverse('scheduler_details', args=[scheduler.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduler_details.html')

    def test_add_test_cases_view(self):
        scheduler = Scheduler.objects.create(name='Test Scheduler', user=self.user)
        url = reverse('add_test_cases', args=[scheduler.id])
        response = self.client.post(url, {'test_cases': [self.test_case.id]})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduler_details.html')

    def test_create_scheduler_view(self):
        url = reverse('create_scheduler')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_scheduler.html')

    def test_remove_test_case_view(self):
        scheduler = Scheduler.objects.create(name='Test Scheduler', user=self.user)
        scheduler.test_cases.add(self.test_case)
        url = reverse('remove_test_case', args=[scheduler.id, self.test_case.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('scheduler_details', args=[scheduler.id]))

    def test_scheduler_history_view(self):
        scheduler = Scheduler.objects.create(user=self.user)
        scheduler_run = SchedulerRun.objects.create(scheduler=scheduler)
        url = reverse('scheduler_history', args=[scheduler.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduler_history.html')
        self.assertEqual(response.context['scheduler'], scheduler)
        self.assertContains(response, scheduler_run.status)

    def test_scheduler_run_history_view(self):
        scheduler = Scheduler.objects.create(user=self.user)
        scheduler_run = SchedulerRun.objects.create(scheduler=scheduler)
        test_run = TestRun.objects.create(test=self.test_case, scheduler_run=scheduler_run)
        url = reverse('scheduler_run_history', args=[scheduler_run.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduler_run_history.html')
        self.assertEqual(response.context['scheduler_run'], scheduler_run)
        self.assertContains(response, test_run.status)

    def test_delete_scheduler_view(self):
        scheduler = Scheduler.objects.create(user=self.user)
        url = reverse('delete_scheduler', args=[scheduler.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertFalse(Scheduler.objects.filter(id=scheduler.id).exists())