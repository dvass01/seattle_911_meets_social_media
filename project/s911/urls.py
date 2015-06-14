from django.conf.urls import patterns, include, url
from django.contrib import admin
from s911.views import IndexView, SeedView

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view(),name="index"),
	url(r'^seed$', SeedView.as_view(),name="seed"),
	# url(r'^instagram_location',InstagramLocationView.as_view(),name = 'instagram_location'),
	# url(r'^instagram_post',InstagramPostView.as_view(),name = 'instagram_post'),

)	