from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import requests
from s911.models import InstagramLocation, Incident, SocrataLocation, InstagramPost   
from project.settings import INSTAGRAM_CLIENT_ID, INSTAGRAM_CLIENT_SECRET, SOCRATA_APP_TOKEN, SOCRATA_SECRET_TOKEN
from urllib import parse
from datetime import datetime, timedelta
from django.utils import timezone

def socrata_time_parser(string):
	year = int(string[0:4])
	month = int(string[5:7])
	day = int(string[8:10])
	hour = int(string[11:13])
	minute = int(string[14:16])
	second = int(string[17:19])
	return timezone.now() - (datetime.now() - datetime(year, month, day, hour, minute, second))

def save_incidents():
	base_url = "https://data.seattle.gov/resource/3k2p-39jp.json"
	params = "?$where=event_clearance_date>=%272015-06-13T18:00:00%27"
	headers = {"X-App-Token":SOCRATA_APP_TOKEN}
	response = requests.get(base_url+params, headers=headers)
	incidents = response.json()

	for incident in incidents:
		clearance_date = socrata_time_parser(incident['event_clearance_date'])
		new_location = SocrataLocation(
			longitude=incident['longitude'],
			latitude=incident['latitude'],
			name=incident['hundred_block_location'],
			)
		new_location.save()
		new_incident = Incident(
			location=new_location,
			clearance_date=incident['event_clearance_date'],
			description=incident['initial_type_description'],
			cad_event_number=incident['cad_event_number'],
			)
		new_incident.save()


def save_instagram_locations():
	incidents = Incident.objects.all()
	for incident in incidents:
		latitude = incident.location.latitude
		longitude = incident.location.longitude
		url = 'https://api.instagram.com/v1/locations/search?lat={}&lng={}&access_token=260141671.59a8916.63821af94cab4cf8a6373d1d8828a4b6'.format(latitude,longitude)
		r = requests.get(url)
		instagram_locations = r.json()['data']
		for location in instagram_locations:
			new_location = InstagramLocation(latitude = location['latitude'], longitude = location['longitude'], name = location['name'], instagram_id = location['id'])
			new_location.save()
			print (location)

def save_instagram_posts():
	instagram_locations = InstagramLocation.objects.all()
	for location in instagram_locations:
		instagram_id = location.instagram_id
		url = 'https://api.instagram.com/v1/locations/{}/media/recent?access_token=260141671.59a8916.63821af94cab4cf8a6373d1d8828a4b6'.format(instagram_id)
		r = requests.get(url)
		instagram_posts = r.json()['data']
		for post in instagram_posts:
			new_post = InstagramPost(location=location,image_url=post['link'])
			new_post.save()
			print (new_post.image_url)

class IndexView(TemplateView):
	template_name = "s911/index.html"

class SeedView(TemplateView):	

	def get(self, request):
		save_incidents()
		save_instagram_locations()
		save_instagram_posts()
		return HttpResponse("success")



