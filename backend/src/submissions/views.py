from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import SubmissionForm, ContestSubmissionForm
from accounts.models import Profile
from problems.models import Problem, TestCase
from contests.models import ContestsHaveProblems, Contest, Participant
from .models import Submission, ContestSubmission, Language, SubmissionTasks
# Create your views here.

def submission_list(request):
	
	submission_list = Submission.objects.filter(user = request.user.profile)
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

def contest_submission_list(request):
	
	contest_submission_list = ContestSubmission.objects.filter(user__user = request.user.profile)
	paginator = Paginator(contest_submission_list,1)
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

def submit_problem(request, *args, **kwargs):
	# form = SubmissionForm(request.POST or None)
	
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

	return render(request, "submissions/problem_submission.html", context)

def submit_contest_problem(request, *args, **kwargs):

	form = ContestSubmissionForm(request.POST or None)
	if form.is_valid():
		print(kwargs['slug2'])
		profile = get_object_or_404(Profile, user = request.user)
		contest = get_object_or_404(Contest, slug = kwargs['slug1'])
		problem = get_object_or_404(Problem, slug = kwargs['slug2'])
		contest_problem = get_object_or_404(ContestsHaveProblems, problem = problem, contest = contest)
		participant = get_object_or_404(Participant, user = profile, contest = contest)
		instance = form.save(commit=False)
		instance.problem = contest_problem
		instance.user = participant
		instance.save()
		return redirect('contest_problem', kwargs['slug1'], kwargs['slug2'])

	context = {
		'form': form,
	}
	return render(request, 'problem_create.html', context)
