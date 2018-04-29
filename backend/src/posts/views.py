from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
 
from .models import Post
from .forms import PostForm

@login_required
def create(request):
	"""
	View to create a post
	"""
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.author = request.user.profile
		form.save_m2m()
		instance.save()

	context = {
		'form': form,
	}
	return render(request, 'posts/post_create.html', context)

def post(request, slug):
	"""
	View for a post
	"""
	instance = get_object_or_404(Post, slug = slug)

	context = {
		'obj': instance,
	}

	return render(request, "posts/post_details.html", context)

def post_list(request):
	"""
	View for a post feed
	"""
	post_list = Post.objects.all()

	if request.method == 'GET':
		tags = request.GET.get('tags')
		title = request.GET.get('title')

		if tags:
			post_list = post_list.filter(tags__in = tags)
		if title:
			post_list = post_list.filter(title__contains=request.GET.get('title'))

	paginator = Paginator(post_list,3)

	page = request.GET.get('page',1)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		'post_list' : queryset
	}

	return render(request, "posts/post_list.html", context)


@login_required
def post_manage(request, slug):
	"""
	View to edit a post
	"""
	instance = get_object_or_404(Post, slug = slug)

	if request.user.profile != instance.author:
		# User != the author
		raise PermissionDenied

	form = PostForm(request.POST or None, instance = instance)
	if form.is_valid() and instance.author == request.user.profile:
		instance = form.save(commit=False)
		form.save_m2m()
		instance.save()

	context = {
		'form': form,
		'obj': instance,
	}
	return render(request, 'posts/post_manage.html', context)


