from django.db import models

from problems.models import Problem
from accounts.models import Profile
from contests.models import ContestsHaveProblems, Participant

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from problems.models import TestCase

# Create your models here


class Language(models.Model):
	""" Language used """
	language_name = models.CharField(max_length=100)

	def __str__(self):
		return self.language_name;

class Submission(models.Model):
	""" Submissions to Normal Problems """

	ACCEPTED_ANSWER = 'AC'
	WRONG_ANSWER = 'WA'
	RUNTIME_ERROR = 'RE'
	TIME_EXCEEDED = 'TLE'
	INTERNAL_ERROR = 'IE'
	RUNNING = 'R'
	COMPILATION_ERROR = 'CE'

	STATUS_CHOICES = (
		(ACCEPTED_ANSWER, 'ACCEPTED'),
		(WRONG_ANSWER, 'WRONG ANSWER'),
		(RUNTIME_ERROR, 'RUNTIME ERROR'),
		(TIME_EXCEEDED, 'TIME LIMIT EXCEEDED'),
		(INTERNAL_ERROR, 'INTERNAL ERROR'),
		(RUNNING, 'RUNNING'),
		(COMPILATION_ERROR, 'COMPILATION_ERROR')
	)

	user = models.ForeignKey(Profile, on_delete = models.CASCADE)
	problem = models.ForeignKey(Problem, on_delete = models.CASCADE)
	code = models.TextField()
	language = models.ForeignKey(Language, blank=True, null=True, on_delete = models.SET_NULL)
	status = models.CharField(max_length=3, choices= STATUS_CHOICES, default = RUNNING)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	testcases = models.ManyToManyField(TestCase, through = 'SubmissionTasks')
	score = models.DecimalField(max_digits=4, decimal_places=2, default=0)

	def __str__(self):
		return "%s-%s-%s"%(self.user.user.username, self.problem.problem_code, self.id)


class ContestSubmission(models.Model):
	""" Submissions to Contest Problems """

	ACCEPTED_ANSWER = 'AC'
	WRONG_ANSWER = 'WA'
	RUNTIME_ERROR = 'RE'
	TIME_EXCEEDED = 'TLE'
	INTERNAL_ERROR = 'IE'
	RUNNING = 'R'

	STATUS_CHOICES = (
		(ACCEPTED_ANSWER, 'ACCEPTED'),
		(WRONG_ANSWER, 'WRONG ANSWER'),
		(RUNTIME_ERROR, 'RUNTIME ERROR'),
		(TIME_EXCEEDED, 'TIME LIMIT EXCEEDED'),
		(INTERNAL_ERROR, 'INTERNAL ERROR'),
		(RUNNING, 'RUNNING')
	)

	user = models.ForeignKey(Participant, on_delete = models.CASCADE)
	problem = models.ForeignKey(ContestsHaveProblems, on_delete = models.CASCADE)
	code = models.TextField()
	language = models.ForeignKey(Language, blank=True, null=True, on_delete = models.SET_NULL)
	status = models.CharField(max_length=3, choices= STATUS_CHOICES, default = RUNNING)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)

	
class SubmissionTasks(models.Model):
	""" Stores results of each submission tast/tetcase """

	ACCEPTED_ANSWER = 'AC'
	WRONG_ANSWER = 'WA'
	RUNTIME_ERROR = 'RE'
	TIME_EXCEEDED = 'TLE'
	INTERNAL_ERROR = 'IE'
	RUNNING = 'R'

	STATUS_CHOICES = (
		(ACCEPTED_ANSWER, 'ACCEPTED'),
		(WRONG_ANSWER, 'WRONG ANSWER'),
		(RUNTIME_ERROR, 'RUNTIME ERROR'),
		(TIME_EXCEEDED, 'TIME LIMIT EXCEEDED'),
		(INTERNAL_ERROR, 'INTERNAL ERROR'),
		(RUNNING, 'RUNNING')
	)

	submission = models.ForeignKey(Submission, on_delete = models.CASCADE)
	testcase = models.ForeignKey(TestCase, on_delete = models.CASCADE)
	status = models.CharField(max_length=3, choices= STATUS_CHOICES, default = RUNNING)

	def __str__(self):
		return "%s-%s-%s"%(self.submission.id, self.testcase.id, self.id)


# class ContestSubmissionTask(models.Model):


