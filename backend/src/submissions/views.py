from django.shortcuts import render, redirect, get_object_or_404

from .forms import SubmissionForm, ContestSubmissionForm
from accounts.models import Profile
from problems.models import Problem
from contests.models import ContestsHaveProblems, Contest, Participant
# Create your views here.

def submit_problem(request, *args, **kwargs):
	form = SubmissionForm(request.POST or None)

	if form.is_valid():

		isParticipant = get_object_or_404(Profile, user = request.user)
		instance = form.save(commit=False)
		instance.user = isParticipant
		instance.problem = get_object_or_404(Problem, slug = kwargs['slug'])
		instance.save()
		return redirect('problem', kwargs['slug'])
	context = {
		'form': form,
	}
	return render(request, 'problem_create.html', context)

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
