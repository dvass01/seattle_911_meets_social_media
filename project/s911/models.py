from django.db import models

# Create your models here.
class Incident(models.Model):
	location = models.ForeignKey('Location', related_name='incidents')
	description = models.CharField(max_length = 100)
	clearance_date = models.DateTimeField()
	cad_event_number = models.CharField(max_length = 20)

	# time = models.DateField()

class Post(models.Model):
	location = models.ForeignKey('Location', related_name='posts')
	# user = models.CharField(max_length=20)
	# created_at = models.DateField()
	#data = models.CharField(max_length = 100)
	# url = models.URLField()

class InstagramPost(Post):
	image_url = models.URLField(max_length=100)

class Location(models.Model):
	latitude = models.DecimalField(max_digits = 15, decimal_places = 12)
	longitude = models.DecimalField(max_digits = 15, decimal_places = 12)

class InstagramLocation(Location):
	instagram_id = models.CharField(max_length = 100)
	name = models.CharField(max_length = 100)

class SocrataLocation(Location):
	name = models.CharField(max_length = 100)

# class FacebookLocation(Location):
# 	name = models.CharField(max_length = 100)


# data = {'latitude':1237894, 'longitude':134235, 'description':'string', 'time':'datetime'}

# try:
# 	location = SocrataLocation.objects.get(latitude=data['latitude'], longitude=data['longitude'])
# except:
# 	location = SocrataLocation(latitude=data['latitude'], longitude=data['longitude'])
# 	location.save()

# incident = Incident(location=location, description=data['description'], time=data['time'])
# incident.save()

# url = "instagram.com/{}/{}".format(incident.location.latitude, incident.location.longitude)

# locations = [{'instagram_id':1, 'latitude':'latitude', 'longitude':'longitude', 'name':'name'}]
# instagram_location = InstagramLocation(name = locations['name'],....)
# instagram_location.save()

# url = "instagram.com/{}".format(instagram_location.instagram_id)

# posts = [{user:"", data:""}]




# latitude = incident.location.latitude


# locations = Location.objects.filter(lat>=i.lat>=lat, long>=i.long>=long)
# for 

# all_incidents = l1.incidents.all()
# all_posts = l1.posts.all()

# incident = Incident.objects.get(id = 11)
# incident.location.posts