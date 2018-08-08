from django.conf.urls import url, include
from . import views
from .api import TagViewSet

from submissions.views import submit_problem

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tags', TagViewSet)


urlpatterns = [
	url(r'^api/', include(router.urls)),
]