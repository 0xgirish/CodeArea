from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect


from .forms import ProblemForm, TestCaseForm
from .models import Problem
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
		'title': instance.title,
		'statement': instance.statement,
	}

	return render(request, "problem_details.html", context)

def problem_list(request):
	if request.GET.get('title'):
		problem_list = Problem.objects.filter(title__contains=request.GET.get('title'))
	else:
		problem_list = Problem.objects.all()
	problem_list1 = Problem.objects.all()
	paginator = Paginator(problem_list,1)

	page = request.GET.get('page',1)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		'problem_list' : queryset,
		'problems' : problem_list1,
	}

	return render(request, "problems/problem_list.html", context)


def add_testcase(request, slug):
	form = TestCaseForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		problem = get_object_or_404(Problem, slug = slug)
		instance.problem_id = problem
		instance.save()

	context = {
		'form':form,
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

