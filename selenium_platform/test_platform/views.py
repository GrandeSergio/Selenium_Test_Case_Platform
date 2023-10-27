from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import TestCase, TestRun, Scheduler, SchedulerRun
from .forms import EditCodeForm, EditTestNameForm, RegistrationForm, SchedulerForm
import subprocess
import logging
from django.contrib import messages
import os
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from selenium import webdriver
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from datetime import datetime


def execute_test_case(test, scheduler_run=None):
    result = subprocess.run(['python', '-m', 'unittest', test.file.path],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output = result.stderr

    # Update the last_run_status and last_run_date fields of the corresponding TestCase object
    if result.returncode == 0:
        test.last_run_status = 'PASSED'
        status = 'PASSED'
    else:
        test.last_run_status = 'FAILED'
        status = 'FAILED'
    test.last_run_date = timezone.now()

    test.console_output = output
    try:
        test.save()
    except Exception as e:
        logging.error(f"Error saving test object: {e}")

    # Create a new TestRun object and save it to the database
    test_run = TestRun(test=test, date=timezone.now(), status=status, output=output, scheduler_run=scheduler_run)
    test_run.save()
    return output


@login_required
def test_list(request):
    # Retrieve the search parameters from the GET request
    search_name = request.GET.get('search_name', '')
    search_script_id = request.GET.get('search_script_id', '')
    search_last_run_status = request.GET.get('search_last_run_status', '')
    search_last_run_date = request.GET.get('search_last_run_date', '')

    # Filter the tests queryset based on the search parameters and the current user
    tests = TestCase.objects.filter(user=request.user)
    if search_name:
        tests = tests.filter(name__icontains=search_name)
    if search_script_id:
        tests = tests.filter(id__icontains=search_script_id)
    if search_last_run_status:
        tests = tests.filter(last_run_status__icontains=search_last_run_status)
    if search_last_run_date:
        tests = tests.filter(last_run_date__icontains=search_last_run_date)

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'name')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'desc':
        tests = tests.order_by(f"-{sort_by}")
    else:
        tests = tests.order_by(sort_by)

    paginator = Paginator(tests, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'test_list.html', {'page_obj': page_obj, 'sort_by': sort_by,
                                              'sort_order': sort_order,
                                              'search_name': search_name,
                                              'search_script_id': search_script_id,
                                              'search_last_run_status': search_last_run_status,
                                              'search_last_run_date': search_last_run_date,
                                              }
                  )


@login_required
def test_details(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    runs = test.testrun_set.order_by('-date')
    file_path = test.file.path if test.file else ''
    file_content = ''

    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

    edit_mode = False
    if 'edit' in request.GET:
        edit_mode = True
        if request.method == 'POST':
            form = EditTestNameForm(request.POST, instance=test)
            if form.is_valid():
                form.save()
                return redirect('test_details', test_id=test.id)
        else:
            form = EditTestNameForm(instance=test)
    else:
        form = EditCodeForm(initial={'code': file_content})

    search_run_id = request.GET.get('search_run_id', '')
    search_last_run_status = request.GET.get('search_last_run_status', '')
    search_last_run_date = request.GET.get('search_last_run_date', '')

    # Filter the tests queryset based on the search parameters
    if search_run_id:
        runs = runs.filter(id__icontains=search_run_id)
    if search_last_run_status:
        runs = runs.filter(status__icontains=search_last_run_status)
    if search_last_run_date:
        try:
            search_date = datetime.strptime(search_last_run_date, '%d-%m-%Y')
            runs = runs.filter(date__date=search_date.date())
        except ValueError:
            # Handle invalid date format if needed
            pass

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'date')
    sort_order = request.GET.get('sort_order', 'desc')
    if sort_order == 'desc':
        runs = runs.order_by(f"-{sort_by}")
    else:
        runs = runs.order_by(sort_by)

    return render(request, 'test_details.html',
                  {'test': test, 'runs': runs, 'form': form, 'file_content': file_content, 'edit_mode': edit_mode,
                   'active_tab': 'details'})


@login_required
def replace_file(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)

    if request.method == 'POST':
        file = request.FILES.get('file')

        if file:
            max_file_size = 10 * 1024 * 1024  # 10MB in bytes
            # File Validation - Allow only .py files
            if not file.name.endswith('.py'):
                return JsonResponse({'success': False, 'error': 'Invalid file format. Only .py files are allowed.'})

            # File Size Limit - Maximum 10MB

            elif file.size > max_file_size:
                return JsonResponse({'success': False, 'error': 'File size exceeds the allowed limit of 10MB.'})

            else:
                # Delete the old file
                if test.file:
                    default_storage.delete(test.file.path)

                # Save the new file
                test.file.save(file.name, ContentFile(file.read()))
                return JsonResponse({'success': True, 'message': 'File replaced successfully.'})

        return JsonResponse({'success': False, 'error': 'Please provide a file.'})

    return redirect('test_details', test_id=test_id)


@login_required
def test_code(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    file_path = test.file.path
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    return render(request, 'test_code.html',
                  {'test': test, 'file_content': file_content, 'active_tab': 'code'})


@login_required
def test_history_list(request):
    user = request.user

    # Filter all TestRun objects associated with the user
    test_runs = TestRun.objects.filter(test__user=user)

    # Retrieve the search parameters from the GET request
    search_run_id = request.GET.get('search_run_id', '')
    search_name = request.GET.get('search_name', '')
    search_script_id = request.GET.get('search_script_id', '')
    search_last_run_status = request.GET.get('search_last_run_status', '')
    search_last_run_date = request.GET.get('search_last_run_date', '')

    # Filter the tests queryset based on the search parameters
    if search_run_id:
        test_runs = test_runs.filter(id__icontains=search_run_id)
    if search_name:
        test_runs = test_runs.filter(name__icontains=search_name)
    if search_script_id:
        test_runs = test_runs.filter(test__id__icontains=search_script_id)
    if search_last_run_status:
        test_runs = test_runs.filter(status__icontains=search_last_run_status)
    if search_last_run_date:
        test_runs = test_runs.filter(date__icontains=search_last_run_date)

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'date')
    sort_order = request.GET.get('sort_order', 'desc')
    if sort_order == 'desc':
        test_runs = test_runs.order_by(f"-{sort_by}")
    else:
        test_runs = test_runs.order_by(sort_by)

    paginator = Paginator(test_runs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'test_history_list.html', {'test_runs': test_runs, 'page_obj': page_obj})


@login_required
def test_history(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    runs = test.testrun_set.order_by('-date')

    search_run_id = request.GET.get('search_run_id', '')
    search_last_run_status = request.GET.get('search_last_run_status', '')
    search_last_run_date = request.GET.get('search_last_run_date', '')

    # Filter the tests queryset based on the search parameters
    if search_run_id:
        runs = runs.filter(id__icontains=search_run_id)
    if search_last_run_status:
        runs = runs.filter(status__icontains=search_last_run_status)
    if search_last_run_date:
        runs = runs.filter(date__icontains=search_last_run_date)

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'date')
    sort_order = request.GET.get('sort_order', 'desc')
    if sort_order == 'desc':
        runs = runs.order_by(f"-{sort_by}")
    else:
        runs = runs.order_by(sort_by)

    # Pagination
    paginator = Paginator(runs, 10)  # Show 10 runs per page
    page = request.GET.get('page')
    try:
        runs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        runs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        runs = paginator.page(paginator.num_pages)

    return render(request, 'test_history.html', {'test': test, 'page_obj': runs, 'active_tab': 'history'})


@login_required
def run_output(request, run_id):
    run = get_object_or_404(TestRun, pk=run_id)
    return render(request, 'run_output.html', {'run': run})


@login_required
def run_test_cases(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)

    output = execute_test_case(test)
    return JsonResponse({'output': output})


@login_required
def delete_test_case(request, test_id):
    test_case = get_object_or_404(TestCase, pk=test_id)
    if request.method == 'POST':
        test_case_path = os.path.join(settings.MEDIA_ROOT, str(test_case.file))
        try:
            os.remove(test_case_path)
            test_case.delete()
            return JsonResponse({'success': True})
        except OSError:
            return JsonResponse({'success': False, 'error_message': 'Failed to delete file'})

    return render(request, 'test_delete.html', {'test': test_case})


'''
@login_required
def upload(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')
        if name and file:
            test_case = TestCase.objects.create(user=request.user, name=name, file=file)
            test_case_url = reverse('test_details', kwargs={'test_id': test_case.id})
            return JsonResponse({'success': True, 'test_case_url': test_case_url})
    return render(request, 'upload.html')
'''


@login_required
def upload(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')
        if name and file:
            # File Validation - Allow only .py files
            if not file.name.endswith('.py'):
                return JsonResponse({'success': False, 'error': 'Invalid file format. Only .py files are allowed.'})

            # File Size Limit - Maximum 10MB
            max_file_size = 10 * 1024 * 1024  # 10MB in bytes
            if file.size > max_file_size:
                return JsonResponse({'success': False, 'error': 'File size exceeds the allowed limit of 10MB.'})

            # Save the test case
            test_case = TestCase.objects.create(user=request.user, name=name, file=file)
            test_case_url = reverse('test_details', kwargs={'test_id': test_case.id})
            return JsonResponse({'success': True, 'test_case_url': test_case_url})

        return JsonResponse({'success': False, 'error': 'Please provide both name and file.'})

    return render(request, 'upload.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('test_list')
        else:
            error_message = 'Invalid username or password.'
            messages.error(request, error_message)  # Add error message to display as a toast
            return render(request, 'login.html')
    return render(request, 'login.html')


@login_required
def user_details(request):
    return render(request, 'user_details.html')


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Additional logic before deleting the account if needed
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('login')  # Redirect to the desired URL after deletion
    else:
        # Handle GET request if needed
        return redirect('user_details')  # Redirect to the user details page


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('change_password')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Add a success message when the password is changed
        messages.success(self.request, 'Password changed successfully.')

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)

        # Add an error message when something went wrong
        messages.error(self.request, 'Failed to change password.')

        return response


@login_required
def scheduler_list(request):
    schedulers = Scheduler.objects.filter(user=request.user)

    search_scheduler_name = request.GET.get('search_scheduler_name', '')  # Update the parameter name
    search_scheduler_id = request.GET.get('search_scheduler_id', '')

    # Filter the tests queryset based on the search parameters and the current user
    if search_scheduler_name:
        schedulers = schedulers.filter(name__icontains=search_scheduler_name)
    if search_scheduler_id:
        schedulers = schedulers.filter(id__icontains=search_scheduler_id)

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'id')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'desc':
        schedulers = schedulers.order_by(f"-{sort_by}")
    else:
        schedulers = schedulers.order_by(sort_by)

    paginator = Paginator(schedulers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = SchedulerForm(request.POST)
        if form.is_valid():
            scheduler = form.save(commit=False)
            scheduler.created_at = timezone.now()
            scheduler.user = request.user  # Assign the current user
            scheduler.save()
            return redirect('scheduler_details', scheduler.id)
    else:
        form = SchedulerForm()

    return render(request, 'scheduler_list.html', {
        'schedulers': page_obj,
        'form': form,
        'page_obj': page_obj,
    })


@login_required
def scheduler_details(request, scheduler_id):
    scheduler = get_object_or_404(Scheduler, pk=scheduler_id, user=request.user)
    test_cases = scheduler.test_cases.all()

    search_name = request.GET.get('search_name', '')
    search_script_id = request.GET.get('search_script_id', '')

    # Filter the tests queryset based on the search parameters and the current user
    if search_name:
        test_cases = test_cases.filter(name__icontains=search_name)
    if search_script_id:
        test_cases = test_cases.filter(id__icontains=search_script_id)

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'name')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'desc':
        test_cases = test_cases.order_by(f"-{sort_by}")
    else:
        test_cases = test_cases.order_by(sort_by)

    paginator = Paginator(test_cases, 12)  # Change the number per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    runs = scheduler.scheduler_runs.all() if scheduler else []

    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'run_all':
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            # mode = 'batch'

            scheduler_run = SchedulerRun.objects.create(scheduler=scheduler, status='Running')

            for test_case in test_cases:
                output = execute_test_case(test_case, scheduler_run)

            # Update the status of the scheduler run once all test cases are executed
            scheduler_run.status = 'Completed'
            scheduler_run.date = timezone.now()
            scheduler_run.save()

            # Redirect to the scheduler details page after running all test cases
            return HttpResponseRedirect(request.path)

    context = {'scheduler': scheduler, 'test_cases': page_obj, 'runs': runs, 'active_tab': 'details'}
    return render(request, 'scheduler_details.html', context)


@login_required
def add_test_cases(request, scheduler_id):
    scheduler = get_object_or_404(Scheduler, pk=scheduler_id)

    search_name = request.GET.get('search_name', '')
    search_script_id = request.GET.get('search_script_id', '')
    search_last_run_status = request.GET.get('search_last_run_status', '')
    search_last_run_date = request.GET.get('search_last_run_date', '')

    # Filter the tests queryset based on the search parameters and the current user
    tests = TestCase.objects.filter(user=request.user)
    if search_name:
        tests = tests.filter(name__icontains=search_name)
    if search_script_id:
        tests = tests.filter(id__icontains=search_script_id)
    if search_last_run_status:
        tests = tests.filter(last_run_status__icontains=search_last_run_status)
    if search_last_run_date:
        tests = tests.filter(last_run_date__icontains=search_last_run_date)

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'name')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'desc':
        tests = tests.order_by(f"-{sort_by}")
    else:
        tests = tests.order_by(sort_by)

    paginator = Paginator(tests, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'GET' and 'test_cases' in request.GET:
        test_case_ids = request.GET.getlist('test_cases')
        selected_test_cases = TestCase.objects.filter(id__in=test_case_ids, user=request.user)
        scheduler.test_cases.add(*selected_test_cases)
        return redirect('scheduler_details', scheduler.id)  # Redirect to the scheduler details page

    context = {
        'scheduler': scheduler,
        'page_obj': page_obj,
        'search_name': search_name,
        'search_script_id': search_script_id,
        'search_last_run_status': search_last_run_status,
        'search_last_run_date': search_last_run_date,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }

    return render(request, 'add_test_cases_modal.html', context)


@login_required
def create_scheduler(request):
    if request.method == 'POST':
        form = SchedulerForm(request.POST)
        if form.is_valid():
            scheduler = form.save(commit=False)
            scheduler.created_at = timezone.now()
            scheduler.user = request.user  # Assign the current user
            scheduler.save()
            return redirect('scheduler_details')
    else:
        form = SchedulerForm()
    return render(request, 'create_scheduler.html', {'form': form})


@login_required
def remove_test_case(request, scheduler_id, testcase_id):
    scheduler = get_object_or_404(Scheduler, id=scheduler_id)
    test_case = get_object_or_404(TestCase, id=testcase_id)

    # Remove the test case from the scheduler
    scheduler.test_cases.remove(test_case)

    return redirect('scheduler_details', scheduler_id=scheduler_id)


@login_required
def scheduler_history(request, scheduler_id):
    user = request.user
    scheduler = get_object_or_404(Scheduler, pk=scheduler_id, user=user)  # Get the scheduler for the logged-in user
    runs = scheduler.scheduler_runs.filter(scheduler__user=user) if scheduler else []

    search_status = request.GET.get('search_status', '')
    search_run_id = request.GET.get('search_run_id', '')

    # Filter the tests queryset based on the search parameters and the current user
    if search_status:
        runs = runs.filter(status__icontains=search_status)
    if search_run_id:
        runs = runs.filter(id__icontains=search_run_id)

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'date')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'desc':
        runs = runs.order_by(f"-{sort_by}")
    else:
        runs = runs.order_by(sort_by)

    # Pagination
    paginator = Paginator(runs, 10)  # Show 10 runs per page
    page = request.GET.get('page')
    try:
        runs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        runs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        runs = paginator.page(paginator.num_pages)

    context = {
        'page_obj': runs,
        'scheduler': scheduler,
        'active_tab': 'history'
    }
    return render(request, 'scheduler_history.html', context)


@login_required
def scheduler_run_history(request, scheduler_run_id):
    scheduler_run = get_object_or_404(SchedulerRun, pk=scheduler_run_id)
    test_runs = TestRun.objects.filter(scheduler_run=scheduler_run)

    search_test_case_id = request.GET.get('search_test_case_id', '')
    search_run_id = request.GET.get('search_run_id', '')
    search_test_case_name = request.GET.get('search_test_case_name', '')
    search_status = request.GET.get('search_status', '')

    # Filter the tests queryset based on the search parameters and the current user
    if search_test_case_id:
        test_runs = test_runs.filter(test__id__icontains=search_test_case_id)
    if search_run_id:
        test_runs = test_runs.filter(id__icontains=search_run_id)
    if search_test_case_name:
        test_runs = test_runs.filter(test__name__icontains=search_test_case_name)
    if search_status:
        test_runs = test_runs.filter(status__icontains=search_status)

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'date')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'desc':
        test_runs = test_runs.order_by(f"-{sort_by}")
    else:
        test_runs = test_runs.order_by(sort_by)

    # Pagination
    paginator = Paginator(test_runs, 10)  # Show 10 runs per page
    page = request.GET.get('page')
    try:
        test_runs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        test_runs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        test_runs = paginator.page(paginator.num_pages)

    return render(request, 'scheduler_run_history.html', {'scheduler_run': scheduler_run, 'page_obj': test_runs})


@login_required
def delete_scheduler(request, scheduler_id):
    scheduler = get_object_or_404(Scheduler, pk=scheduler_id)
    if request.method == 'POST':

        try:

            scheduler.delete()
            return JsonResponse({'success': True})
        except OSError:
            return JsonResponse({'success': False, 'error_message': 'Failed to delete scheduler'})

    return JsonResponse({'success': False, 'error_message': 'Invalid request'})
