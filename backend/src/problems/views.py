from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


from .forms import ProblemForm, TestCaseForm
from .models import Problem, TestCase
# Create your views here.

@login_required
def create(request):
	"""
	View to create a problem
	"""
	form = ProblemForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.setter = request.user.profile
		instance.save()

	context = {
		'form': form,
	}
	return render(request, 'problems/problem_create.html', context)

def problem(request, slug):
	"""
	View for a problem page
	"""
	instance = get_object_or_404(Problem, slug = slug)

	context = {
		'obj' : instance,
	}

	return render(request, "problems/problem_details.html", context)

def problem_list(request):
	"""
	View for a problem feed
	"""

	problem_list = Problem.objects.filter(unlisted = False)

	if request.method == 'GET':
		level = request.GET.get('level')
		tags = request.GET.get('tags')
		title = request.GET.get('title')

		if level and level != 'All':
			problem_list = problem_list.filter(level = level.upper())
		if tags:
			problem_list = problem_list.filter(tags__in = tags)
		if title:
			problem_list = problem_list.filter(title__contains=request.GET.get('title'))

	paginator = Paginator(problem_list,2)

	page = request.GET.get('page',1)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		'problem_list' : queryset,
	}

	return render(request, "problems/problem_list.html", context)

@login_required
def add_testcase(request, slug):
	"""
	View to add testcases to a problem
	"""
	form = TestCaseForm(request.POST or None)
	problem = get_object_or_404(Problem, slug = slug)

	if request.user.profile != problem.setter:
		# Only problem setter can add testcases
		raise PermissionDenied

	testcases = TestCase.objects.filter(problem_id = problem)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.problem_id = problem
		instance.save()

	context = {
		'form':form,
		'obj': problem,
		'testcases': testcases,

	}
	return render(request,"problems/add_testcase.html", context)


@login_required
def problem_manage(request, slug):
	"""
	View to manage a problem
	"""

	instance = get_object_or_404(Problem, slug = slug)

	if request.user.profile != instance.setter:
		# Only problem setter edit problem
		raise PermissionDenied

	form = ProblemForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'form': form,
		'obj': instance,
	}
	return render(request, 'problems/problem_manage.html', context)


def ide(request):
	return render(request, 'problems/code.html',{})

