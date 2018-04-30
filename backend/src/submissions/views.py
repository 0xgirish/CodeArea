from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from .forms import SubmissionForm, ContestSubmissionForm
from accounts.models import Profile
from problems.models import Problem, TestCase
from contests.models import ContestsHaveProblems, Contest, Participant
from .models import Submission, ContestSubmission, Language, SubmissionTasks
# Create your views here.
from django.http import Http404


@login_required
def submission_list(request):
	"""
	view for a list of user submissions
	"""
	
	submission_list = Submission.objects.filter(user = request.user.profile).order_by('-timestamp')
	paginator = Paginator(submission_list,10)
	page = request.GET.get('page',1)
	try:
		submission_list = paginator.page(page)
	except PageNotAnInteger:
		submission_list = paginator.page(1)
	except EmptyPage:
		submission_list = paginator.page(paginator.num_pages)

	context = {
		'submission_list' : submission_list,
	}

	return render(request, "submissions/submission_list.html", context)

@login_required
def problem_submission_list(request,slug):
	"""
	view for a list of user submissions for a problem
	"""
	problem = get_object_or_404(Problem, slug = slug)
	submission_list = Submission.objects.filter(user = request.user.profile, problem__slug = slug).order_by('-timestamp')
	paginator = Paginator(submission_list,10)
	page = request.GET.get('page',1)
	try:
		submission_list = paginator.page(page)
	except PageNotAnInteger:
		submission_list = paginator.page(1)
	except EmptyPage:
		submission_list = paginator.page(paginator.num_pages)

	context = {
		'submission_list' : submission_list,
		'obj' : problem,
	}

	return render(request, "submissions/problem_submission_list.html", context)


@login_required
def contest_submission_list(request):
	"""
	View for a list of contet submission of a user
	"""
	contest_submission_list = ContestSubmission.objects.filter(user__user = request.user.profile).order_by('-timestamp')
	paginator = Paginator(contest_submission_list,10)
	page = request.GET.get('page',1)
	try:
		contest_submission_list = paginator.page(page)
	except PageNotAnInteger:
		contest_submission_list = paginator.page(1)
	except EmptyPage:
		contest_submission_list = paginator.page(paginator.num_pages)

	context = {
		'contest_submission_list' : contest_submission_list,
	}

	return render(request, "submissions/contest_submission_list.html", context)


def contest_problem_submission(request, slug1, slug2):
	"""
	View for contest problem submission
	:params slug1: contest slug
	:params slug2: problem slug
	"""
	contest = get_object_or_404(Contest, slug = slug1)
	problem = get_object_or_404(Problem, slug = slug2)
	contest_problem = get_object_or_404(ContestsHaveProblems, contest= contest, problem = problem )
	contest_submission_list = ContestSubmission.objects.filter(user__user = request.user.profile, problem = contest_problem).order_by('-timestamp')
	paginator = Paginator(contest_submission_list,10)
	page = request.GET.get('page',1)
	try:
		contest_submission_list = paginator.page(page)
	except PageNotAnInteger:
		contest_submission_list = paginator.page(1)
	except EmptyPage:
		contest_submission_list = paginator.page(paginator.num_pages)

	context = {
		'queryset' : contest_submission_list,
		'contest': contest,
		'obj': problem,
	}

	return render(request, "contests/contest_problem_submission.html", context)

@login_required
def submit_problem(request, *args, **kwargs):
	"""
	View for problem submit
	:params slug: problem slug
	"""
	context = {}
	problem = get_object_or_404(Problem, slug = kwargs['slug'])
	testcases = TestCase.objects.filter(problem = problem)
	if request.method == 'POST':
		isParticipant = get_object_or_404(Profile, user = request.user)
		print(request.POST.get('lang'))

		lang = get_object_or_404(Language, language_name = request.POST.get('lang'))
		print(problem.problem_code)

		instance = Submission()
		instance.user = isParticipant
		instance.problem = problem
		instance.code = request.POST.get('code')
		instance.language = lang
		instance.save()
		# print("done")
		

		context = {
			'obj': problem,
			'submission': instance,
			'lang': lang,
		}
	else:
		raise Http404("Submission not Found")

	return render(request, "submissions/problem_submission.html", context)

@login_required
def submit_contest_problem(request, *args, **kwargs):
	"""
	View for submitting a contest problem
	:params slug1: contest slug
	:params slug2: problem slug
	"""
	context = {}
	contest = get_object_or_404(Contest, slug = kwargs['slug1'])
	problem = get_object_or_404(Problem, slug = kwargs['slug2'])
	testcases = TestCase.objects.filter(problem = problem)
	contest_problem = get_object_or_404(ContestsHaveProblems, problem = problem, contest = contest)

	if request.method == 'POST':
		isParticipant = get_object_or_404(Participant, user = request.user.profile, contest = contest)
		lang = get_object_or_404(Language, language_name = request.POST.get('lang'))
		instance = ContestSubmission()
		instance.user = isParticipant
		instance.problem = contest_problem
		instance.code = request.POST.get('code')
		instance.language = lang
		instance.save()

		context = {
			'obj': problem,
			'submission': instance,
			'contest': contest,
			'lang': lang,
		}

	else:
		raise Http404("Submission not Found")

	return render(request, 'submissions/contest_problem_submission.html', context)
