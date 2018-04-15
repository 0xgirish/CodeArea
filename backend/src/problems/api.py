from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect


from .forms import ProblemForm, TestCaseForm
from .models import Problem, TestCase

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets


from .permissions import IsOwnerOrReadOnly

from .serializers import TestCaseSerializer


class TestCaseViewSet(viewsets.ModelViewSet):
	
	queryset = TestCase.objects.all()
	serializer_class = TestCaseSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)