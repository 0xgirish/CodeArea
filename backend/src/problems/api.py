from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect


from .forms import ProblemForm, TestCaseForm
from .models import Problem, TestCase 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import generics, filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.filters import SearchFilter


from .permissions import IsOwnerOrReadOnly

from .serializers import TestCaseSerializer, ProblemSerializer


class TestCaseViewSet(viewsets.ModelViewSet):
	
	queryset = TestCase.objects.all()
	serializer_class = TestCaseSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
	parser_classes = (MultiPartParser, FormParser,)



class ProblemViewSet(viewsets.ModelViewSet):

	queryset = Problem.objects.all()
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ProblemSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filter_fields = ('problem_code',)
	search_fields = ('title', 'problem_code',)

