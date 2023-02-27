from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import TestCase
from  .forms import TestUploadForm

def test_list(request):
    tests = TestCase.objects.all()
    return render(request, 'test_list.html', {'tests': tests})

def test_details(request, test_id):
    test = get_object_or_404(TestCase, pk=test_id)
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
