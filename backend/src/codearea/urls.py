"""codearea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import isworking
from problems.views import ide
from judge.views import run_judge

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^problems/', include('problems.urls')),
    url(r'^contests/', include('contests.urls')),
    url(r'^submissions/', include('submissions.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^posts/', include('posts.urls')),
    url(r'^api/', include('rest_framework.urls')),
    url(r'^tags/', include('tags.urls')),
    url(r'^ide/$', ide, name='ide'),
    url(r'^judge', run_judge),
    url(r'$', isworking),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
