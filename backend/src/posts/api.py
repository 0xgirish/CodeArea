from django.shortcuts import render, get_object_or_404, redirect

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

from .serializers import PostSerializer

from .models import Post
from .permissions import IsOwnerOrReadOnly


class PostLikeAPIToggle(APIView):
	
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, slug, format=None):
		"""
		Return a list of all users.
		"""
		instance = get_object_or_404(Post, slug = slug)
		url_ = instance.get_absolute_url()
		user = self.request.user
		updated  = False
		liked = False
		if user.is_authenticated():
			if user.profile in instance.likes.all():
				instance.likes.remove(user.profile)
				liked = False
			else:
				instance.likes.add(user.profile)
				liked = True

			updated = True

		count = instance.likes.all().count()
		data = {
			"updated" : updated,
			"liked": liked,
			"count": count
		}

		return Response(data)



class PostViewSet(viewsets.ModelViewSet):
	
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	authentication_classes = (authentication.SessionAuthentication,)
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
	parser_classes = (MultiPartParser, FormParser,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	search_fields = ('title',)

