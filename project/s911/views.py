from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import requests
from math import radians, cos, sin, asin, sqrt
from s911.models import InstagramLocation, Incident, SocrataLocation, InstagramPost, Location, Post   
from project.settings import INSTAGRAM_CLIENT_ID, INSTAGRAM_CLIENT_SECRET, SOCRATA_APP_TOKEN, SOCRATA_SECRET_TOKEN, CARTODB_API_KEY
from urllib import parse
from datetime import datetime, timedelta
from django.utils import timezone
import os

def socrata_time_parser(string):
	year = int(string[0:4])
	month = int(string[5:7])
	day = int(string[8:10])
	hour = int(string[11:13])
	minute = int(string[14:16])
	second = int(string[17:19])
	return timezone.now() - (datetime.now() - datetime(year, month, day, hour, minute, second))

def cartodb_time_parse(datetime_object):
	year = str(datetime_object.year)
	month = str(datetime_object.month)
	day = str(datetime_object.day)
	hour = str(datetime_object.hour)
	minute = str(datetime_object.minute)
	second = str(datetime_object.second)
	return year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + "Z"


	# 2011-01-11T01:11:11Z

def save_incidents():
	base_url = "https://data.seattle.gov/resource/3k2p-39jp.json"
	params = "?$where=event_clearance_date>=%272015-06-14T16:00:00%27"
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


def save_instagram_locations_and_posts():
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
			url = 'https://api.instagram.com/v1/locations/{}/media/recent?access_token=260141671.59a8916.63821af94cab4cf8a6373d1d8828a4b6'.format(new_location.instagram_id)
			r = requests.get(url)
			instagram_posts = r.json()['data']
			for post in instagram_posts:
				new_post = InstagramPost(location=new_location,image_url=post['link'],incident = incident)
				new_post.save()

def clean_database():
	incidents = Incident.objects.all()
	incidents.delete()
	locations = Location.objects.all()
	locations.delete()
	posts = Post.objects.all()
	posts.delete()

class IndexView(TemplateView):
	template_name = "s911/index.html"

class SeedView(TemplateView):	

	def get(self, request):
		save_incidents()
		save_instagram_locations_and_posts()
		return HttpResponse("success")

def cartodb_sql_incident():
	incidents = Incident.objects.all()
	for incident in incidents:
		clearance_date = cartodb_time_parse(incident.clearance_date)
		SQL_INSERT = "INSERT INTO incident (id, cad_event_number, clearance_date, description, latitude, longitude, location_name) "
		SQL_VALUES = "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(incident.id, incident.cad_event_number, clearance_date, incident.description, incident.location.latitude, incident.location.longitude, incident.location.socratalocation.name)
		SQL_statement = SQL_INSERT + SQL_VALUES
		url = 'https://dvass1994.cartodb.com/api/v2/sql?q={}&api_key={}'.format(SQL_statement, CARTODB_API_KEY)
		response = requests.post(url)
	print(response.json())
	return response

def cartodb_sql_incident_delete():
	incidents = Incident.objects.all()
	SQL_statement = "DELETE FROM incident"
	url = 'https://dvass1994.cartodb.com/api/v2/sql?q={}&api_key={}'.format(SQL_statement, CARTODB_API_KEY)
	response = requests.post(url)
	print(response.json())
	return response	

class CartodbIncident(TemplateView):

	def get(self, request):
		cartodb_sql_incident_delete()
		cartodb_sql_incident()
		return redirect("/")


def cartodb_sql_instagram_post():
	instagram_posts = InstagramPost.objects.all()
	for instagram_post in instagram_posts:
		SQL_INSERT = "INSERT INTO instagram_post (id, image_url, instagram_id, latitude, longitude, location_name) "
		SQL_VALUES = "VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(instagram_post.id, instagram_post.image_url, instagram_post.location.instagramlocation.instagram_id, instagram_post.location.latitude, instagram_post.location.longitude, instagram_post.location.instagramlocation.name)
		SQL_statement = SQL_INSERT + SQL_VALUES
		url = 'https://dvass1994.cartodb.com/api/v2/sql?q={}&api_key={}'.format(SQL_statement, CARTODB_API_KEY)
		response = requests.post(url)
	print(response.json())
	return response

class CartodbInstagramPost(TemplateView):

	def get(self, request):
		cartodb_sql_instagram_post()
		return redirect("/")

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r		

class Timeline(TemplateView):

	def get(self, request):
		print (request)
		incident_id = request.GET['id']
		i = Incident.objects.get(id=incident_id)
		all_posts = i.posts.all()
		posts = []
		for post in all_posts:
			print (post.instagrampost.image_url, post.location.instagramlocation.name)
			post_dict = {'image_url':post.instagrampost.image_url, 'location_name':post.location.instagramlocation.name}
			posts.append(post_dict)
		print (posts)
		context_dict = {'incident':{'description':i.description, 'clearance_date' : i.clearance_date, 'location_name' : i.location.socratalocation.name}, 'posts' : posts}	
		print (context_dict)
		return JsonResponse(context_dict)






