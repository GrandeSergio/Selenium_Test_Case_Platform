from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import TestCase, TestRun
from .forms import TestUploadForm, EditCodeForm, EditTestNameForm
import subprocess
from django.middleware.csrf import get_token
import logging
from django.contrib import messages
import os, sys, io
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
from selenium import webdriver
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def test_list(request):
    sort_by = request.GET.get('sort_by', 'name')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'asc':
        tests = TestCase.objects.all().order_by(sort_by)
    else:
        tests = TestCase.objects.all().order_by(f'-{sort_by}')
    paginator = Paginator(tests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'test_list.html', {'page_obj': page_obj, 'sort_by': sort_by, 'sort_order': sort_order})

def replace_file(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)

    if request.method == 'POST':
        file = request.FILES.get('file')

        if file:
            # Delete the old file
            if test.file:
                default_storage.delete(test.file.path)

            # Save the new file
            test.file.save(file.name, ContentFile(file.read()))

    return redirect('test_details', test_id=test_id)

def test_details(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    runs = test.testrun_set.order_by('-date')
    file_path = test.file.path
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

    return render(request, 'test_details.html',
                  {'test': test, 'runs': runs, 'form': form, 'file_content': file_content, 'edit_mode': edit_mode})


def test_history_list(request):
    test_runs = TestRun.objects.all().order_by('-date')
    return render(request, 'test_history_list.html', {'test_runs': test_runs})


def run_output(request, run_id):
    run = get_object_or_404(TestRun, pk=run_id)
    return render(request, 'run_output.html', {'run': run})


def test_upload(request):
    if request.method == 'POST':
        form = TestUploadForm(request.POST, request.FILES)
        if form.is_valid():
            test_case = form.save(commit=False)
            test_case.save()
            return redirect('test_details', test_id=test_case.id)
    else:
        form = TestUploadForm()
    return render(request, 'test_upload.html', {'form': form})


def run_test_cases(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)

    # Get the mode selected by the user
    mode = request.POST.get('mode')

    if mode == 'batch':
        # Run the script in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    else:
        # Run the script in windowed mode
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

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
    test_run = TestRun(test=test, date=timezone.now(), status=status, output=output)
    test_run.save()

    return JsonResponse({'output': output})



def test_history(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    runs = test.testrun_set.order_by('-date')
    return render(request, 'test_history.html', {'test': test, 'runs': runs})


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