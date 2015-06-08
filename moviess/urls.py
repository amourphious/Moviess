"""moviess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from moviess.views import get_all, getMovieById, getMovie, addMovie, updateMovie, deleteMovie, manageAdmin, renderHome, createDummyDB

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^createdummy/', createDummyDB),
    url(r'^$', renderHome),
    url(r'^movies/all/$', get_all),
    url(r'^movies/(\d+)/$', getMovieById),
    url(r'^movies/search/$', getMovie),
    url(r'^movies/add/$', addMovie),
    url(r'^movies/update/(\d+)/$', updateMovie),
    url(r'^movies/delete/(\d+)/$', deleteMovie),
    url(r'^admin/([^/]{1,30})/$', manageAdmin),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
