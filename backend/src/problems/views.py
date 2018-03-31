from django.shortcuts import render, get_object_or_404, redirect


from .forms import ProblemForm
from .models import Problem
# Create your views here.

def create(request):
	form = ProblemForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'form': form,
	}
	return render(request, 'problem_create.html', context)

def problem(request, slug):
	instance = get_object_or_404(Problem, slug = slug)

	context = {
		'title': instance.title,
		'statement': instance.statement,
	}

	return render(request, "problem_details.html", context)

def problem_list(request):
	queryset = Problem.objects.all() 
	context = {
		'problem_list' : queryset
	}

	return render(request, "problems/problem_list.html", context)

