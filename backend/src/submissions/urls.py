from django.conf.urls import url, include
from . import views
from problems.views import problem
from . import api

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'submission', api.SubmissionViewSet)
router.register(r'subtask', api.SubmissionTasksViewSet)
router.register(r'contestsubmission', api.ContestSubmissionViewSet)
router.register(r'contest/subtask', api.ContestSubmissionTasksViewSet)


urlpatterns = [
	# url(r'^submit/', views.submit, name='submit_problem'),
	url(r'^$', views.submission_list, name='submission_list'),
	url(r'^contest/$', views.contest_submission_list, name='contest_submission_list'),
	url(r'^api/', include(router.urls)),
	url(r'^problem/(?P<slug>[-\w]+)/', views.problem_submission_list, name='problem_submission_list'),
	

]