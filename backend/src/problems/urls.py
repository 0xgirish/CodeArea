from django.conf.urls import url, include
from . import views
from .api import TestCaseViewSet, ProblemViewSet

from submissions.views import submit_problem, problem_submission_list

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'testcase', TestCaseViewSet)
router.register(r'problem', ProblemViewSet)


urlpatterns = [
	url(r'^create/', views.create, name='create_problem'),
	url(r'^(?P<slug>[-\w]+)/$', views.problem, name='problem'),
	url(r'^(?P<slug>[-\w]+)/submit/$', submit_problem, name='problem_submission'),
	url(r'^(?P<slug>[-\w]+)/manage/$', views.problem_manage, name='problem_manage'),
	url(r'^(?P<slug>[-\w]+)/manage/testcase/$', views.add_testcase, name='problem_testcase'),
	url(r'^(?P<slug>[-\w]+)/manage/submissions/$', views.view_submissions, name='view_submissions'),
	url(r'^(?P<slug>[-\w]+)/manage/delete/$', views.delete_problem, name='delete_problem'),
	url(r'^$', views.problem_list, name='problem_list'),
	url(r'^api/', include(router.urls)),
]