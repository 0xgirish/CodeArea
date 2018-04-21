from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import generics, filters
from .serializers import ContestsHaveProblemsSerializer, ContestSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Contest, ContestsHaveProblems, Participant
from problems.models import Problem
from rest_framework import viewsets
from rest_framework import status

import datetime


class OnGoingContest(filters.BaseFilterBackend):
	"""
	Filter that only allows users to see their own objects.
	"""
	def filter_queryset(self, request, queryset, view):
		date = datetime.datetime.today()
		return queryset.filter(end_contest__gt=date)


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

class ContestProblemViewSet(viewsets.ModelViewSet):
	
	queryset = ContestsHaveProblems.objects.all()
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ContestsHaveProblemsSerializer
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('contest', 'problem')

class ContestViewSet(viewsets.ModelViewSet):

	queryset = Contest.objects.all()
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ContestSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter, )
	filter_fields = ('creator',)
	search_fields = ('contest_code', 'title',)

class OnGoingContestViewSet(viewsets.ModelViewSet):

	queryset = Contest.objects.all()
	
	serializer_class = ContestSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter, OnGoingContest, OrderingFilter)
	filter_fields = ('creator',)
	search_fields = ('contest_code', 'title',)
	ordering = ('end_contest',)




		
