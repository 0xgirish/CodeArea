from django.conf.urls import url, include
from . import views

from . import api

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', api.SubmissionViewSet)


urlpatterns = [
	# url(r'^submit/', views.submit, name='submit_problem'),
	url(r'^$', views.submission_list, name='submission_list'),
	url(r'^contest/$', views.contest_submission_list, name='contest_submission_list'),
	url(r'^api/', include(router.urls)),
]