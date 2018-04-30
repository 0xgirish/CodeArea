# Django related imports
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


# App related imports
from .forms import ContestForm
from .models import Contest, ContestsHaveProblems, Participant
from submissions.models import ContestSubmission



@login_required
def create(request):
	""" 
	View to create a contest
	"""
	form = ContestForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.creator = request.user.profile
		instance.save()

	context = {
		'form': form,
	}
	return render(request, 'contests/contest_create.html', context)

def problem(request, slug1, slug2):
	"""
	View for a contest problem
	:params slug1: contest slug
	:params slug2: problem slug
	"""
	cproblem = get_object_or_404(ContestsHaveProblems, problem__slug = slug2, contest__slug = slug1)
	context = {
		'obj' : cproblem.problem,
		'contest': cproblem.contest,
	}

	return render(request, "contests/problem_details.html", context)

def problem_list(request, slug):
	"""
	View of the contest page showing the list of problems
	"""
	contest = get_object_or_404(Contest, slug = slug)
	participant_list = Participant.objects.filter(contest = contest.id).order_by('-points')[:5:1]
	queryset = ContestsHaveProblems.objects.filter(contest = contest) 
	context = {
		'contest': contest,
		'problem_list' : queryset,
		'participant_list' : participant_list
	}

	return render(request, "contests/contest_details.html", context)

def contest_list(request):
	"""
	View for the contest feed
	"""
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

def leaderboard(request, slug):
	"""
	View for a contest leaderboard
	:params slug: contest slug
	"""
	instance = get_object_or_404(Contest, slug = slug)
	participant_list = Participant.objects.filter(contest = instance.id).order_by('-points')
	paginator = Paginator(participant_list,10)

	page = request.GET.get('page',1)
	try:
		queryset = paginator.page(page)
		rank = (int(page)-1)*10
	except PageNotAnInteger:
		queryset = paginator.page(1)
		rank = 0
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
		rank = 0

	context = {
		'title' : instance.title,
		'slug' : slug,
		'participant_list' : queryset,
		'rank' : rank,
	}
	return render(request, "contests/leaderboard.html", context)

@login_required
def manage_contest(request, slug):
	"""
	View for an admin panel of a contest
	"""
	instance = get_object_or_404(Contest, slug = slug)

	if request.user.profile != instance.creator:
		# Only the creator has permission to edit
		raise PermissionDenied

	form = ContestForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'obj': instance,
		'form': form,
	}

	return render(request, "contests/manage_contest.html",context)

@login_required
def add_problems(request, slug):
	"""
	Adding problems to a contest
	"""
	instance = get_object_or_404(Contest, slug = slug)

	if request.user.profile != instance.creator:
		# Only the creator has permission to add
		raise PermissionDenied

	queryset = ContestsHaveProblems.objects.filter(contest = instance) 
	context = {
		'obj': instance,
		'queryset': queryset,
	}

	return render(request, "contests/add_problems.html",context)

@login_required
def view_submissions(request, slug):
	"""
	View for contest submissions
	"""
	instance = get_object_or_404(Contest, slug = slug)
	if request.user.profile != instance.creator:
		# Only the creator has permission to view
		raise PermissionDenied
	queryset = ContestSubmission.objects.filter(problem__contest = instance)

	context = {
		'obj': instance,
		'queryset': queryset
	}

	return render(request, "contests/contest_submissions.html", context)




