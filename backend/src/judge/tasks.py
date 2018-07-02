from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .index import judge_main
from .contest import judge_main_contest


# TOOD: change return HttpResponse func judge_main*

@shared_task
def task_main(request):
	judge_main(request)

@shared_task
def task_contest(request):
	judge_main_contest(request)
