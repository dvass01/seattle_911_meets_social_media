from django.conf.urls import patterns, include, url
from django.contrib import admin
from s911.views import IndexView, SeedView, CartodbIncident, CartodbInstagramPost, Timeline

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view(),name="index"),
	url(r'^seed$', SeedView.as_view(),name="seed"),
	url(r'^cartodb/incident$', CartodbIncident.as_view(),name="cartodb_incident"),
	url(r'^cartodb/instagrampost$', CartodbInstagramPost.as_view(),name="cartodb_instagrampost"),
	url(r'^timeline$', Timeline.as_view(),name="timeline"),

	# url(r'^instagram_location',InstagramLocationView.as_view(),name = 'instagram_location'),
	# url(r'^instagram_post',InstagramPostView.as_view(),name = 'instagram_post'),

)	

