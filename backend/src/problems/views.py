from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect


from .forms import ProblemForm, TestCaseForm
from .models import Problem, TestCase
# Create your views here.

def create(request):
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
	instance = get_object_or_404(Problem, slug = slug)

	context = {
		'obj' : instance,
	}

	return render(request, "problems/problem_details.html", context)

def problem_list(request):

	problem_list = Problem.objects.all()

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


def add_testcase(request, slug):
	form = TestCaseForm(request.POST or None)
	problem = get_object_or_404(Problem, slug = slug)
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

def problem_manage(request, slug):
	instance = get_object_or_404(Problem, slug = slug)
	form = ProblemForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		'form': form,
		'obj': instance,
	}
	return render(request, 'problems/problem_manage.html', context)

