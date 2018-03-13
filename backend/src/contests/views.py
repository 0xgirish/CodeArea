from django.shortcuts import render, get_object_or_404, redirect

from .forms import ContestForm
# Create your views here.
from .models import Contest, ContestsHaveProblems

def create(request):
	form = ContestForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'form': form,
	}
	return render(request, 'problem_create.html', context)

def problem(request, slug1, slug2):
	cproblem = get_object_or_404(ContestsHaveProblems, problem__slug = slug2, contest__slug = slug1)
	print(contest)
	context = {
		'title': cproblem.problem.title,
		'statement': cproblem.problem.statement,
	}

	return render(request, "problem_details.html", context)

def problem_list(request, slug):
	contest = get_object_or_404(Contest, slug = slug)
	queryset = ContestsHaveProblems.objects.filter(contest = contest) 
	context = {
		'problem_list' : queryset
	}

	return render(request, "contest_problem_list.html", context)

def contest_list(request):
	queryset = Contest.objects.all()
	context = {
		'contest_list' : queryset
	}
	return render(request, "contest_list.html", context)
