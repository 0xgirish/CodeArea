from django.conf.urls import url
from . import views, api

urlpatterns = [
	url(r'^create/', views.create, name='create_posy'),
	url(r'^(?P<slug>[-\w]+)/$', views.post, name='post'),
	url(r'^(?P<slug>[-\w]+)/manage/$', views.post_manage, name='post_manage'),
	url(r'^api/(?P<slug>[-\w]+)/likes/$', api.PostLikeAPIToggle.as_view(), name='post_likes_api'),
	url(r'^$', views.post_list, name='post_list'),
]