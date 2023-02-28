from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import TestCase
from .forms import TestUploadForm
import subprocess
from django.middleware.csrf import get_token



def test_list(request):
    tests = TestCase.objects.all()
    return render(request, 'test_list.html', {'tests': tests})

#def test_details(request, test_id):
#    test = get_object_or_404(TestCase, pk=test_id)
#    return render(request, 'test_details.html', {'test': test})

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

'''
def run_test_cases(request):
    if request.method == 'POST':
        # Get the uploaded file
        file = request.FILES.get('file')

        # Check if file is a Python file
        if file.name.endswith('.py'):
            # Save the file to a temporary location
            with open('temp.py', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Run the file using subprocess module
            result = subprocess.run(['python', 'temp.py'], capture_output=True, text=True)

            # Get the output of the script
            output = result.stdout

            # Render the output in a template
            return render(request, 'test_details.html', {'output': output})
        else:
            # Render an error message if file is not a Python file
            return render(request, 'test_details.html', {'error': 'File must be a Python file.'})
    else:
        return render(request, 'test_details.html')
'''
def run_test_cases(request, test_id):
    if request.method == 'POST':
        test_case = get_object_or_404(TestCase, pk=test_id)
        # Get the CSRF token
        csrf_token = get_token(request)
        # Get the file contents
        file_contents = test_case.file.read()
        # Create a new namespace for the test case
        namespace = {'csrfmiddlewaretoken': csrf_token, 'file_contents': file_contents}
        # Run the test case
        result = exec(file_contents, namespace)
        return HttpResponse(result)
    else:
        return ("Only POST requests are allowed")