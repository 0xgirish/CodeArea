from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ContestForm
# Create your views here.
from .models import Contest, ContestsHaveProblems, Participant
from submissions.models import ContestSubmission

def create(request):
	form = ContestForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.setter = request.user.profile
		instance.save()

	context = {
		'form': form,
	}
	return render(request, 'contests/contest_create.html', context)

def problem(request, slug1, slug2):
	cproblem = get_object_or_404(ContestsHaveProblems, problem__slug = slug2, contest__slug = slug1)
	context = {
		'title': cproblem.problem.title,
		'statement': cproblem.problem.statement,
	}

	return render(request, "problem_details.html", context)

def problem_list(request, slug):
	contest = get_object_or_404(Contest, slug = slug)
	queryset = ContestsHaveProblems.objects.filter(contest = contest) 
	context = {
		'contest': contest,
		'problem_list' : queryset
	}

	return render(request, "contests/contest_details.html", context)

def contest_list(request):
	contest_list = Contest.objects.all()
	paginator = Paginator(contest_list,1)

	page = request.GET.get('page',1)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		'contest_list' : queryset
	}
	return render(request, "contests/contests.html", context)


def manage_contest(request, slug):
	instance = get_object_or_404(Contest, slug = slug)

	form = ContestForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'obj': instance,
		'form': form,
	}

	return render(request, "contests/manage_contest.html",context)


def add_problems(request, slug):
	instance = get_object_or_404(Contest, slug = slug)
	queryset = ContestsHaveProblems.objects.filter(contest = instance) 

	context = {
		'obj': instance,
		'queryset': queryset,
	}

	return render(request, "contests/add_problems.html",context)

def view_submissions(request, slug):
	instance = get_object_or_404(Contest, slug = slug)
	queryset = ContestSubmission.objects.filter(problem__contest = instance)

	context = {
		'obj': instance,
		'queryset': queryset
	}

	return render(request, "contests/contest_submissions.html", context)




