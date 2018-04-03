from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm

from django.views.generic import RedirectView
# Create your views here.
def create(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'form': form,
	}
	return render(request, 'posts/post_create.html', context)

def post(request, slug):
	instance = get_object_or_404(Post, slug = slug)

	context = {
		'obj': instance,
	}

	return render(request, "post_details.html", context)

def post_list(request):
	queryset = Post.objects.all() 
	context = {
		'post_list' : queryset
	}

	return render(request, "posts/post_list.html", context)


class PostLikeToggleView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get("slug")
		instance = get_object_or_404(Post, slug = slug)
		url_ = instance.get_absolute_url()
		user = self.request.user
		if user.is_authenticated():
			if user.profile in instance.likes.all():
				instance.likes.remove(user.profile)
			else:
				instance.likes.add(user.profile)

		return url_

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

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


