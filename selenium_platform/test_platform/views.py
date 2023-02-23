from django.shortcuts import render, redirect
from .forms import TestCaseForm
from .models import TestCase


def home(request):
    if request.method == 'POST':
        form = TestCaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TestCaseForm()

    testcases = TestCase.objects.all()
    context = {'form': form, 'testcases': testcases}
    return render(request, 'home.html', context)


