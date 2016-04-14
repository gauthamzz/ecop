from django.conf.urls import url
from django.contrib import admin
from .views import (
	complaint_create,
	complaint_detail,
	complaint_list,
	complaint_update,
	)

urlpatterns = [
	url(r'^createcomplaint$',complaint_create),
	url(r'^$', complaint_list,name="list"),
	url(r'^(?P<id>\d+)/edit$', complaint_update,name="update"),
	url(r'^(?P<id>\d+)/$', complaint_detail,name="detail"),
	#url(r'^(?P<id>\d+)/delete$', post_delete),
]
