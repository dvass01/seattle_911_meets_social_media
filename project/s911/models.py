from django.db import models

class Incident(models.Model):
	location = models.ForeignKey('Location', related_name='incidents')
	description = models.CharField(max_length = 500)
	clearance_date = models.DateTimeField()
	cad_event_number = models.CharField(max_length = 20)

class Post(models.Model):
	location = models.ForeignKey('Location', related_name='posts')
	incident = models.ForeignKey('Incident', related_name = 'posts')
	created_time = models.DateTimeField()

class InstagramPost(Post):
	image_url = models.URLField(max_length=200)
	post_url = models.URLField(max_length=200)

class Location(models.Model):
	latitude = models.DecimalField(max_digits = 15, decimal_places = 12)
	longitude = models.DecimalField(max_digits = 15, decimal_places = 12)

class InstagramLocation(Location):
	instagram_id = models.CharField(max_length = 100)
	name = models.CharField(max_length = 100)

class SocrataLocation(Location):
	name = models.CharField(max_length = 100)