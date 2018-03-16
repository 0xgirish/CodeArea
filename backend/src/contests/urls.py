from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/', views.create, name='create_contest'),
	url(r'^(?P<slug1>[-\w]{1,100})/problems/(?P<slug2>[-\w]+)/$', views.problem, name='contest_problem'),
	url(r'^(?P<slug>[-\w]+)/$', views.problem_list, name='contest_problem_list'),
	url(r'^$', views.contest_list, name='contest_list'),
]