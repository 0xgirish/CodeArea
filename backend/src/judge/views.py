from django.shortcuts import render

# Create your views here.

from .index import judge_main

def run_judge(request):
    judge_main(request)