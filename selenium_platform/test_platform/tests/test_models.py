from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import TestCase as TestCaseModel, SchedulerRun, TestRun, Scheduler
from django.core.files.storage import default_storage


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

        self.test_case = TestCaseModel.objects.create(
            user=self.user,
            name='Unit Test Case Models 1',
            file='unit_test_models.py',
            last_run_status='Success',
            console_output='Some console output',
            upload_date=timezone.now(),
            last_run_date=timezone.now()
        )
        self.scheduler = Scheduler.objects.create(
            user=self.user,
            name='Test Scheduler',
            created_at=timezone.now(),
            last_run_date=timezone.now()
        )
        self.scheduler_run = SchedulerRun.objects.create(
            scheduler=self.scheduler,
            date=timezone.now(),
            status='Completed'
        )
        self.test_run = TestRun.objects.create(
            test=self.test_case,
            date=timezone.now(),
            status='Passed',
            output='Some output',
            scheduler_run=self.scheduler_run
        )

    def tearDown(self):
        # Delete the files created during the test
        default_storage.delete('unit_test_models.py')

    def test_test_case(self):
        self.assertEqual(self.test_case.user, self.user)
        self.assertEqual(self.test_case.name, 'Test Case Models 1')
        self.assertEqual(self.test_case.file, 'unit_test_models.py')
        self.assertEqual(self.test_case.last_run_status, 'Success')
        self.assertEqual(self.test_case.console_output, 'Some console output')

    def test_scheduler_run(self):
        self.assertEqual(self.scheduler_run.scheduler, self.scheduler)
        self.assertEqual(self.scheduler_run.status, 'Completed')

    def test_test_run(self):
        self.assertEqual(self.test_run.test, self.test_case)
        self.assertEqual(self.test_run.status, 'Passed')
        self.assertEqual(self.test_run.output, 'Some output')
        self.assertEqual(self.test_run.scheduler_run, self.scheduler_run)

    def test_scheduler(self):
        self.assertEqual(self.scheduler.user, self.user)
        self.assertEqual(self.scheduler.name, 'Test Scheduler')
