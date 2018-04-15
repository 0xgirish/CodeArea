from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import generics, filters
from .serializers import ContestsHaveProblemsSerializer
from django_filters.rest_framework import DjangoFilterBackend

from .models import Contest, ContestsHaveProblems, Participant
from problems.models import Problem
from rest_framework import viewsets


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

	def destroy(self, request, *args, **kwargs):
		try:
			instance = self.get_object()
			self.perform_destroy(instance)
		except Http404:
			pass
		return Response(status=status.HTTP_204_NO_CONTENT)



		