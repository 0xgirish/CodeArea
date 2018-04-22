from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from .models import Tag 

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


from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
	
	queryset = Tag.objects.all()
	serializer_class = TagSerializer
	filter_backends = (DjangoFilterBackend, SearchFilter)
	search_fields = ('name',)

