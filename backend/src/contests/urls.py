from django.conf.urls import url, include
from . import views
from submissions.views import submit_contest_problem, contest_problem_submission

from . import api

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'c/p', api.ContestProblemViewSet)
router.register(r'c/ongoing', api.OnGoingContestViewSet)
router.register(r'c', api.ContestViewSet)

urlpatterns = [
	url(r'^create/', views.create, name='create_contest'),
	url(r'^(?P<slug1>[-\w]{1,100})/problems/(?P<slug2>[-\w]+)/$', views.problem, name='contest_problem'),
	url(r'^(?P<slug1>[-\w]{1,100})/problems/(?P<slug2>[-\w]+)/submissions/', contest_problem_submission, name='contest_problem_submissions'),
	url(r'^(?P<slug1>[-\w]{1,100})/problems/(?P<slug2>[-\w]+)/submit/', submit_contest_problem, name='contest_problem_submission'),
	url(r'^(?P<slug1>[-\w]{1,100})/problems/(?P<slug2>[-\w]+)/leaderboard/', views.leaderboard_contest_problem, name='leaderboard_contest_problem'),
	url(r'^(?P<slug>[-\w]+)/$', views.contest_home, name='contest_problem_list'),
	url(r'^(?P<slug>[-\w]+)/leaderboard/$', views.leaderboard, name='leaderboard'),
	url(r'^(?P<slug>[-\w]+)/manage/$', views.manage_contest, name='manage_contest'),
	url(r'^(?P<slug>[-\w]+)/manage/problems/$', views.add_problems, name='add_problems'),
	url(r'^(?P<slug>[-\w]+)/manage/delete/$', views.delete_contest, name='delete_contest'),
	url(r'^(?P<slug>[-\w]+)/manage/submissions/$', views.view_submissions, name='contest_submissions'),
	url(r'^$', views.contest_list, name='contest_list'),
	url(r'^api/(?P<slug>[-\w]+)/signup/$', api.ContestSignUpAPI.as_view(), name='contest_signup_api'),
	url(r'^api/contest/', include(router.urls)),

	
]