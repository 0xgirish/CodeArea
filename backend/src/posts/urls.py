from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/', views.create, name='create_posy'),
	url(r'^(?P<slug>[-\w]+)/$', views.post, name='post'),
	url(r'^(?P<slug>[-\w]+)/likes/$', views.PostLikeToggleView.as_view(), name='post_likes'),
	url(r'^api/(?P<slug>[-\w]+)/likes/$', views.PostLikeAPIToggle.as_view(), name='post_likes_api'),
	url(r'^$', views.post_list, name='post_list'),
]