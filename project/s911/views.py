from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import requests
from s911.models import InstagramLocation 
# Create your views here.
#from instagram.client import InstagramAPI
from project.settings import INSTAGRAM_CLIENT_ID, INSTAGRAM_CLIENT_SECRET

##get the code

#	'https://api.instagram.com/oauth/authorize/?client_id=59a89166252a4fd68fac55b1cbb4c6c4&redirect_uri=http://127.0.0.1:8000/redirect&response_type=code'


##find location id
#https://api.instagram.com/v1/locations/search?lat=47.659333&lng=-122.347990&access_token=260141671.59a8916.63821af94cab4cf8a6373d1d8828a4b6

## find posts
#https://api.instagram.com/v1/locations/250336103/media/recent?access_token=260141671.59a8916.63821af94cab4cf8a6373d1d8828a4b6

class IndexView(TemplateView):
	template_name = "s911/index.html"

class InstagramLocationView(TemplateView):
	def get(self, request):
		latitude = '47.613655'
		longitude = '-122.345003'
		url = 'https://api.instagram.com/v1/locations/search?lat={}&lng={}&access_token=260141671.59a8916.63821af94cab4cf8a6373d1d8828a4b6'.format(latitude,longitude)
		r = requests.get(url)
		instagram_locations = r.json()['data']
		for location in instagram_locations:
			new_location = InstagramLocation(latitude = location['latitude'], longitude = location['longitude'], name = location['name'], instagram_id = location['id'])
			new_location.save()
			print (location)
		return HttpResponseRedirect(url)

class InstagramPostView(TemplateView):
	def get(self, request):
		instagram_id = '2382142'
		url = 'https://api.instagram.com/v1/locations/{}/media/recent?access_token=260141671.59a8916.63821af94cab4cf8a6373d1d8828a4b6'.format(instagram_id)
		r = requests.get(url)
		print (r.json()['data'][0]['link'])
		print (r.json()['data'][1]['link'])
		print (r.json()['data'][2]['link'])
		return HttpResponseRedirect(url)		
