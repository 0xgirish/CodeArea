from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .tasks import *
from .normal import judge_main_normal

# TODO: return current submission page with submission id

@login_required
def run_judge(request):
	data = request.POST.get("submit")
	data_dict = json.loads(data)
	submission_id = data_dict['submission_id']
	result = task_main(data)
    # return judge_main(request)

@login_required
def run_judge_contest(request):
	data = request.POST.get("submit")
	data_dict = json.loads(data)
	submission_id = data_dict['submission_id']
	result = task_contest(data)
    # return judge_main_contest(request)

@login_required
def run_judge_normal(request):
    return judge_main_normal(request)
