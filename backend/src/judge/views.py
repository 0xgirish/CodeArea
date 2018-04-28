from django.shortcuts import render

# Create your views here.

from .index import judge_main
from .contest import judge_main_contest

def run_judge(request):
    return judge_main(request)

def run_judge_contest(request):
    return judge_main_contest(request)