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


def test_details(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    runs = test.testrun_set.order_by('-date')
    if request.method == 'POST':
        # Temporarily disable button to prevent double-click
        return HttpResponse()
        # output = run_test_cases(request, test_id)
        # return JsonResponse({'output': output})
    return render(request, 'test_details.html', {'test': test, 'runs': runs})


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
    print('run_test_cases called')
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