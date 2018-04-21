from django.conf.urls import url
from . import views

urlpatterns = [
	# url(r'^submit/', views.submit, name='submit_problem'),
	url(r'^$', views.submission_list, name='submission_list'),
	url(r'^contest/$', views.contest_submission_list, name='contest_submission_list'),
]