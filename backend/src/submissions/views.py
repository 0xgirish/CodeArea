from django.shortcuts import render

from .forms import SubmissionForm
# Create your views here.

def submit(request):
	form = SubmissionForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'form': form,
	}
	return render(request, 'problem_create.html', context)
