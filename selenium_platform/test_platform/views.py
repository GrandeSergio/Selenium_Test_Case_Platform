from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import TestCase
from .forms import TestUploadForm
import subprocess
from django.middleware.csrf import get_token
import logging
from django.contrib import messages


def test_list(request):
    tests = TestCase.objects.all()
    return render(request, 'test_list.html', {'tests': tests})


def test_details(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    if request.method == 'POST':
        # Run the uploaded script
        result = subprocess.run(['python', test.file.path], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
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
    if request.method == 'POST':
        test = get_object_or_404(TestCase, pk=test_id)
        # Get the CSRF token
        csrf_token = get_token(request)
        # Get the file contents
        file_contents = test.file.read()
        # Create a new namespace for the test case
        namespace = {'csrfmiddlewaretoken': csrf_token, 'file_contents': file_contents}
        # Run the test case
        try:
            result = exec(file_contents, namespace)
            messages.info(request, f'Test cases for test "{test.name}" are being run...')
            if result == "success":
                print("success")
                test.last_run_status = "success"
            elif result == "failed":
                print("failed")
                test.last_run_status = "failed"
            else:
                print('none')
                test.last_run_status = "none"
            test.save()
            return JsonResponse({'result': result})
        except Exception as e:
            messages.error(request, f'Test cases for test "{test.name}" failed to run.')
            logging.exception("Error running test")
            return JsonResponse({'result': 'error'})
    else:
        return HttpResponse("Only POST requests are allowed")

def delete_test_case(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
    test.delete()
    return JsonResponse({'success': True})