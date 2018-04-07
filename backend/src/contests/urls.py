from django.conf.urls import url
from . import views
from submissions.views import submit_contest_problem

urlpatterns = [
	url(r'^create/', views.create, name='create_contest'),
	url(r'^(?P<slug1>[-\w]{1,100})/problems/(?P<slug2>[-\w]+)/$', views.problem, name='contest_problem'),
	url(r'^(?P<slug1>[-\w]{1,100})/problems/(?P<slug2>[-\w]+)/submit/', submit_contest_problem, name='contest_problem_submission'),
	url(r'^(?P<slug>[-\w]+)/$', views.problem_list, name='contest_problem_list'),
	url(r'^(?P<slug>[-\w]+)/manage/$', views.manage_contest, name='manage_contest'),
	url(r'^$', views.contest_list, name='contest_list'),
	url(r'^api/(?P<slug>[-\w]+)/$', views.ContestSignUpAPI.as_view(), name='contest_signup_api'),
]