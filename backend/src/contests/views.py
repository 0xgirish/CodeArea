from django.shortcuts import render, get_object_or_404, redirect

from .forms import ContestForm
# Create your views here.
from .models import Contest, ContestsHaveProblems, Participant

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
	queryset = Contest.objects.all()
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
		'contest': instance,
		'form': form,
	}

	return render(request, "contests/manage_contest.html",context)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class ContestSignUpAPI(APIView):
	
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, slug, format=None):
		"""
		Return a list of all users.
		"""
		instance = get_object_or_404(Contest, slug = slug)
		user = self.request.user
		signed_up = False
		if user.is_authenticated():
			if user.profile in instance.participants.all():
				signed_up = True
			else:
				Participant.objects.create(contest = instance, user = user.profile)
				signed_up = True

		data = {
			"signup" : signed_up,
		}

		return Response(data)
