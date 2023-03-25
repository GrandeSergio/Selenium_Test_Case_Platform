from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import TestCase, TestRun
from .forms import TestUploadForm
import subprocess
from django.middleware.csrf import get_token
import logging
from django.contrib import messages
import os, sys, io
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone


def test_list(request):
    tests = TestCase.objects.all()
    paginator = Paginator(tests, 15)  # Show 10 tests per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'test_list.html', {'page_obj': page_obj})


def test_details(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    if request.method == 'POST':
        output = run_test_cases(test)
        return JsonResponse({'output': output})
    return render(request, 'test_details.html', {'test': test})


def test_upload(request):
    if request.method == 'POST':
        form = TestUploadForm(request.POST, request.FILES)
        if form.is_valid():
            test_case = form.save()
            return redirect('test_details', test_id=test_case.id)
    else:
        form = TestUploadForm()
    return render(request, 'test_upload.html', {'form': form})


def run_test_cases(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    # Run the uploaded script
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
    test.save()

    # Create a new TestRun object and save it to the database
    test_run = TestRun(test=test, date=timezone.now(), status=status, output=output)
    test_run.save()

    return JsonResponse({'output': output})

def test_history(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    runs = test.testrun_set.order_by('-date')
    return render(request, 'test_history.html', {'test': test, 'runs': runs})

'''
def run_test_cases(request, test_id):
    if request.method == 'POST':
        test = get_object_or_404(TestCase, pk=test_id)
        # Get the file contents
        file_contents = test.file.read()
        test_code = file_contents.decode('utf-8')
        # Create a dictionary to store the execution environment
        env = {'request': request, 'test': test}

        # Execute the test case code and capture the output
        result = subprocess.run(["python", "-c", test_code], capture_output=True, text=True)

        # Check the result of the test and update the test status
        if result.returncode == 0:
            test.last_run_status = 'success'
            messages.success(request, f'Test cases for test "{test.name}" ran successfully.')
        else:
            test.last_run_status = 'failed'
            messages.error(request, f'Test cases for test "{test.name}" failed to run:\n{result.stderr}')

        test.save()

        # Render the response
        return JsonResponse({'result': test.last_run_status, 'logs': result.stdout})
    else:
        return HttpResponse("Only POST requests are allowed")
'''

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

def upload(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')
        if name and file:
            test_case = TestCase.objects.create(name=name, file=file)
            test_case_url = reverse('test_details', kwargs={'test_id': test_case.id})
            return JsonResponse({'success': True, 'test_case_url': test_case_url})
    return render(request, 'upload.html')