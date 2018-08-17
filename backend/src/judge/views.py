from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .tasks import *
from .normal import judge_main_normal
import json

# TODO: return current submission page with submission id

@login_required
def run_judge(request):
	data = request.POST.get("submit")
	data_dict = json.loads(data)
	submission_id = data_dict['submission_id']
	task_main.delay(data)
	return HttpResponse(json.dumps({"submission_id": submission_id}))

@login_required
def run_judge_contest(request):
	data = request.POST.get("submit")
	data_dict = json.loads(data)
	submission_id = data_dict['submission_id']
	task_contest.delay(data)
	return HttpResponse(json.dumps({"submission_id": submission_id}))

@login_required
def run_judge_normal(request):
	return judge_main_normal(request)
