from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/', views.create, name='create_problem'),
	url(r'^(?P<slug>[-\w]+)/', views.problem, name='problem'),
	url(r'^$', views.problem_list, name='problem_list'),
]